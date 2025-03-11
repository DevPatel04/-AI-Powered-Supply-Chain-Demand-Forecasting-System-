import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt import get_prompt, get_prompt_update , get_prompt_with_old_data
from agent import get_sales_report

# Configure page settings
st.set_page_config(page_title="Supply Chain Demand Forecasting Chatbot", layout="wide")
st.title("Supply Chain Demand Forecasting Chatbot")

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


# Sidebar navigation and model selection
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
    ["gemini-2.0-pro-exp-02-05", "gemini-2.0-flash-thinking-exp-01-21", "llama-3.1-8b-instant"]
)

st.session_state.input_data["data"] = st.sidebar.selectbox("Do you have the last 3 months of data?", ["No", "Yes"])

if model_name == "llama-3.1-8b-instant":
    llm = ChatGroq(model=model_name, temperature=0.5)
else:
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.5)

# Collect input data
if not st.session_state.input_data_set:
    with st.form(key="input_form"):
        st.session_state.input_data["industry"] = st.text_input("Enter the industry:")
        if st.session_state.input_data["data"] == "Yes":
            csv_path = st.file_uploader("Upload a CSV file", type="csv")
            st.session_state.input_data["old_data"] = get_sales_report(csv_path)
            st.session_state.input_data['products'] = " "
        else:
            st.session_state.input_data["products"] = st.text_input("Enter the Products")
        st.session_state.input_data["location"] = st.text_input("Enter the location:")
        st.session_state.input_data["timeframe"] = st.text_input("Enter the timeframe:")
        st.session_state.input_data["type_of_business"] = st.selectbox("Enter the type of business:", ["Retail", "Manufacturing", "Wholesale", "Other"])
        st.session_state.input_data["size_of_business"] = st.selectbox("Enter the size of business:", ["Small", "Medium", "Large", "Extra Large"])
        
        submit_button = st.form_submit_button(label="Submit")
    
    if submit_button:
        missing_fields = [key for key, value in st.session_state.input_data.items() if not value and key != "old_data"]
        
        if st.session_state.input_data["data"] == "Yes" and not csv_path:
            st.warning("Please upload a CSV file as you selected 'Yes' for historical data.")
        elif missing_fields:
            st.warning(f"Please fill out all fields before submitting: {', '.join(missing_fields).replace('_', ' ').title()}")
        else:
            st.session_state.input_data_set = True
            st.success("Form submitted successfully!")

# Generate prompt
def generate_prompt(user_input):
    if not st.session_state.first_response:

        prompt = get_prompt(st.session_state.input_data)
        st.session_state.first_response = True
        first_data = ""

        for key, value in st.session_state.input_data.items():
            first_data = first_data+f"{key}: {value}\n"

        st.session_state.chat_history.append({"role": "user", "content": first_data})

    if st.session_state.input_data["data"] == "Yes":
        print("data")
        prompt = get_prompt_with_old_data(st.session_state.input_data)
        st.session_state.first_response = True
        first_data = ""
        
        for key, value in st.session_state.input_data.items():
            if key != "old_data":
                first_data = first_data+f"{key}: {value} \n\n"
                
        st.session_state.chat_history.append({"role": "user", "content": first_data})
    else:
        prompt = get_prompt(st.session_state.input_data)
        # prompt = get_prompt_update(st.session_state.input_data, user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

    return ChatPromptTemplate.from_messages([
        ("system", "You are an expert supply chain demand forecaster."),
        ("human",prompt)
    ])

def display_chat_history():
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Handle chat
if st.session_state.input_data_set:
    st.session_state.user_input = st.chat_input("Type your response here")
    prompt_template = generate_prompt(st.session_state.user_input)
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

# Reset button
if st.sidebar.button("Reset Chat"):
    st.session_state.clear()
    st.rerun()