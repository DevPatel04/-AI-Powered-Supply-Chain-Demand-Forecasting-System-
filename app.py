import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt import get_prompt, get_prompt_update

# Configure page settings
st.set_page_config(page_title="Website Maker Chatbot", layout="wide")
st.title("Website Maker Chatbot")

# Load API key
def load_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except KeyError:
        st.error("GROQ API Key not found. Please add it to your Streamlit secrets.")
        st.stop()

GROQ_API_KEY = load_api_key()

# Initialize session state
def init_session_state():
    default_values = {
        "input_data": {"industry": "", "products": "", "location": "", "data": "", "timeframe": ""},
        "input_data_set": False,
        "conversation_chain": None,
        "first_response": False,
        "user_input": '',
        "chat_history": []
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Sidebar navigation and model selection
def sidebar_navigation():
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

    return st.sidebar.selectbox(
        "Select Model", 
        ["gemini-2.0-pro-exp-02-05", "gemini-2.0-flash-thinking-exp-01-21", "llama-3.1-8b-instant"]
    )

model_name = sidebar_navigation()

# Initialize language model
def initialize_llm(model_name):
    return ChatGroq(model=model_name, temperature=0.5) if model_name == "llama-3.1-8b-instant" else ChatGoogleGenerativeAI(model=model_name, temperature=0.5)

llm = initialize_llm(model_name)

# Collect input data
def collect_input():
    if not st.session_state.input_data_set:
        with st.form(key="input_form"):
            for field in st.session_state.input_data:
                st.session_state.input_data[field] = st.text_input(f"Enter the {field.replace('_', ' ')}:")
            submit_button = st.form_submit_button(label="Submit")
            if submit_button and all(st.session_state.input_data.values()):
                st.session_state.input_data_set = True
                st.session_state.first_response = False
            elif submit_button:
                st.warning("Please fill out all fields before submitting.")

collect_input()

# Generate prompt
def generate_prompt(user_input):
    if not st.session_state.first_response:
        prompt = get_prompt(st.session_state.input_data)
        st.session_state.first_response = True
    else:
        prompt = get_prompt_update(st.session_state.input_data, user_input)

    return ChatPromptTemplate.from_messages([
        ("system", "You are an expert-powered supply chain demand forecaster."),
        ("human",prompt)
    ])


# Handle chat
if st.session_state.input_data_set:
    st.session_state.user_input = st.chat_input("Type your response here")
    prompt_template = generate_prompt(st.session_state.user_input)
    st.session_state.chat_history.append({"role": "user", "content": st.session_state.user_input})
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

# Display chat history
def display_chat_history():
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if st.session_state.chat_history:
    display_chat_history()

# This structure makes your app more modular and easier to extend! 🚀
