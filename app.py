# Import all required libraries
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt import get_prompt, get_prompt_update , get_prompt_with_old_data
from agent import get_sales_report

# Configure page settings
st.set_page_config(page_title="Supply Chain Demand Forecasting Chatbot", layout="wide")
st.title("Supply Chain Demand Forecasting Chatbot")


# getting the api kay from secrets
try:    
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("GROQ API Key not found. Please add it to your Streamlit secrets.")
    st.stop()

# Initialize session state
if "input_data" not in st.session_state:
    st.session_state.input_data = {
        "industry": "",
        "products": "",
        "location": "",
        "data": "",
        "timeframe": "",
        "type_of_business": "",
        "size_of_business": "",
        "old_data" : ""
        }
if "input_data_set" not in st.session_state:
    st.session_state.input_data_set = False

if "conversation_chain" not in st.session_state:
    st.session_state.conversation_chain = None

if "first_response" not in st.session_state:
    st.session_state.first_response = False

if "user_input" not in st.session_state:
    st.session_state.user_input = ''

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Sidebar navigation and model selection and checking old data availability
st.sidebar.header("Navigation & Settings")
steps = """
    1.  Enter the industry,
    2.  Enter the products/services,
    3.  Enter the location,
    4.  Enter the data constraints,
    5.  Enter the timeframe
"""

st.sidebar.markdown("**Steps:**")
st.sidebar.markdown(steps)

model_name = st.sidebar.selectbox(
    "Select Model", 
    ["gemini-2.0-pro-exp-02-05", "gemini-2.0-flash-thinking-exp-01-21", "llama3-70b-8192"]
)

st.session_state.input_data["data"] = st.sidebar.selectbox("Do you have the last 3 months of data?", ["No", "Yes"])

# Initialize LLM
if model_name == "llama3-70b-8192":
    llm = ChatGroq(model=model_name, temperature=0.5)
else:
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.5)

# Collect all input data from user

# checking the input is set or not
if not st.session_state.input_data_set: 

    with st.form(key="input_form"):
        st.session_state.input_data["industry"] = st.text_input("Enter the industry:")
        if st.session_state.input_data["data"] == "Yes": # checking the if data is available then showing the file uploader
            csv_path = st.file_uploader("Upload a CSV file", type="csv")
            st.session_state.input_data["old_data"] = get_sales_report(csv_path) # calling the get_sales_report function and storing the output in old_data key
            st.session_state.input_data['products'] = " " # setting the products key to empty string
        else:
            st.session_state.input_data["products"] = st.text_input("Enter the Products")
        st.session_state.input_data["location"] = st.text_input("Enter the location:")
        st.session_state.input_data["timeframe"] = st.text_input("Enter the timeframe:")
        st.session_state.input_data["type_of_business"] = st.selectbox("Enter the type of business:", ["Retail", "Manufacturing", "Wholesale", "Other"])
        st.session_state.input_data["size_of_business"] = st.selectbox("Enter the size of business:", ["Small", "Medium", "Large", "Extra Large"])
        
        submit_button = st.form_submit_button(label="Submit")
    
    if submit_button:
        missing_fields = [key for key, value in st.session_state.input_data.items() if not value and key != "old_data"] # checking the missing fields
        
        if st.session_state.input_data["data"] == "Yes" and not csv_path: # checking the if data is available then showing the file uploader
            st.warning("Please upload a CSV file as you selected 'Yes' for historical data.")
        elif missing_fields: # checking the missing fields 
            st.warning(f"Please fill out all fields before submitting: {', '.join(missing_fields).replace('_', ' ').title()}")
        else:
            st.session_state.input_data_set = True
            st.success("Form submitted successfully!")

def generate_prompt(user_input):
    """This function generate prompt according to data availability of user."""
    # checking the first response is set or not
    if not st.session_state.first_response:
        if st.session_state.input_data["data"] == "Yes": # checking the if data is available then calling the get_prompt_with_old_data function
            prompt = get_prompt_with_old_data(st.session_state.input_data)
            st.session_state.first_response = True
            first_data = ""
        else:
            prompt = get_prompt(st.session_state.input_data)
            st.session_state.first_response = True
            first_data = ""
            
        for key, value in st.session_state.input_data.items():
            first_data = first_data+f"{key}: {value}\n"
        st.session_state.chat_history.append({"role": "user", "content": first_data}) # appending the first data to chat history
    else:
        prompt = get_prompt_update(st.session_state.input_data, user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input}) # appending the user input to chat history

    return ChatPromptTemplate.from_messages([
        ("system", "You are an expert supply chain demand forecaster."),
        ("human",prompt)
    ])

def display_chat_history():
    """This function display chat history"""
    for message in st.session_state.chat_history: # looping through the chat history
        with st.chat_message(message["role"]): # displaying the chat message
            st.markdown(message["content"]) # displaying the content

# Get user input, get response form LLM and display to user 
if st.session_state.input_data_set: # checking the input data set or not
    st.session_state.user_input = st.chat_input("Type your response here") # getting the user input
    prompt_template = generate_prompt(st.session_state.user_input) # generating the prompt
    if st.session_state.chat_history: 
        display_chat_history() 
    with st.spinner("Thinking..."):
        try:
            st.session_state.conversation_chain = prompt_template | llm 
            response = st.session_state.conversation_chain.invoke({"user_input": st.session_state.user_input})
            assistant_response = response.get("text") if isinstance(response, dict) else getattr(response, "content", "Sorry, I couldn’t understand that.")
        except Exception as e:
            assistant_response = f"An error occurred: {e}"
        st.subheader("Response")
        st.markdown(assistant_response)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

# Reset button for clearing chat history in session state
if st.sidebar.button("Reset Chat"):
    st.session_state.clear()
    st.rerun()