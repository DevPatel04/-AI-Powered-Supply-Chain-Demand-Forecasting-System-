import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure secrets and page settings
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("GROQ API Key not found. Please add it to your Streamlit secrets.")

st.set_page_config(page_title="Website Maker Chatbot", layout="wide")
st.title("Website Maker Chatbot")

# Sidebar: Navigation and Model Selection
st.sidebar.header("Navigation & Settings")
steps = [
    "Enter the industry:",
    "Enter the products/services:",
    "Enter the location:",
    "Enter the data constraints:",
    "Enter the timeframe:"
]
st.sidebar.markdown("**Steps:**")
for i, step in enumerate(steps, start=1):
    st.sidebar.markdown(f"{i}. {step}")

model_name = st.sidebar.selectbox(
    "Select Model", 
    ["llama-3.1-8b-instant", "gemini-2.0-pro-exp-02-05", "gemini-2.0-flash-thinking-exp-01-21"]
)

# Initialize session state
if "input_data" not in st.session_state:
    st.session_state.input_data = {
        "industry": "",
        "products": "",
        "location": "",
        "data": "",
        "timeframe": ""
    }
if "input_data_set" not in st.session_state:
    st.session_state.input_data_set = False

if "conversation_chain" not in st.session_state:
    st.session_state.conversation_chain = None

if "first_response" not in st.session_state:
    st.session_state.first_response = False

if "user_input" not in st.session_state:
    st.session_state.user_input = ''

# Initialize the chosen LLM
if model_name == "llama-3.1-8b-instant":
    llm = ChatGroq(model=model_name, temperature=0.5)
else:
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.5)

st.header("Input Details")

# Use a form to collect all inputs at once
if not st.session_state.input_data_set:
    with st.form(key="input_form"):
        st.session_state.input_data["industry"] = st.text_input("Enter the industry:")
        st.session_state.input_data["products"] = st.text_input("Enter the products/services:")
        st.session_state.input_data["location"] = st.text_input("Enter the location:")
        st.session_state.input_data["data"] = st.text_input("Enter the data constraints:")
        st.session_state.input_data["timeframe"] = st.text_input("Enter the timeframe:")

        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            if not all(st.session_state.input_data.values()):
                st.warning("Please fill out all fields before submitting.")
            else:
                st.session_state.input_data_set = True
                st.session_state.first_response = False
else:
    st.session_state.user_input = st.chat_input("Type your response here")

if st.session_state.input_data_set:
    st.subheader("Input Summary")
    for key, value in st.session_state.input_data.items():
        st.markdown(f"**{key.capitalize().replace('_', ' ')}:** {value}")

    # Build the prompt for the LLM
    if not st.session_state.first_response:
        prompt = f"""
        **Context:**

        - **Industry:** {st.session_state.input_data['industry']}
        - **Products/Services:** {st.session_state.input_data['products']}
        - **Location:** {st.session_state.input_data['location']}
        - **Data Constraints:** {st.session_state.input_data['data']}
        - **Timeframe:** {st.session_state.input_data['timeframe']}

        **Task:**
        Act as an expert demand forecaster and supply chain strategist for the given industry. 
        Create a detailed stock/resource list for the business operating in the specified location within the defined timeframe, considering the constraints of available data.
        """
        st.session_state.first_response = True
    else:
        prompt = f"""
        Please modify only the following sections based on the new requirements:
        - {st.session_state.user_input}
        """

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert-powered supply chain demand forecaster."),
        ("human", prompt)
    ])

    st.subheader("Generating Response...")
    with st.spinner("Thinking..."):
        try:
            st.session_state.conversation_chain = prompt_template | llm
            response = st.session_state.conversation_chain.invoke({"user_input": st.session_state.user_input})

            if isinstance(response, dict) and "text" in response:
                assistant_response = response["text"]
            elif response and hasattr(response, "content"):
                assistant_response = response.content
            else:
                assistant_response = "Sorry, I couldn’t understand that."
        except Exception as e:
            assistant_response = f"An error occurred: {e}"

    st.subheader("Response")
    st.markdown(assistant_response)

# Add a reset button
if st.sidebar.button("Reset Chat"):
    st.session_state.clear()
    st.experimental_rerun()

st.sidebar.info("Built with ❤️ using Streamlit and LangChain")

# Let me know if you want to refine this or add new features! 🚀
