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
if "messages" not in st.session_state:
    st.session_state.messages = []

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
                st.session_state.messages = []
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Thank you for providing the necessary details! I’ll start by creating a demand forecast and stock/resource list for your business. Let me generate the initial plan based on the provided inputs... 🚀"
                })

if st.session_state.input_data_set:
    st.subheader("Input Summary")
    for key, value in st.session_state.input_data.items():
        st.markdown(f"**{key.capitalize().replace('_', ' ')}:** {value}")

    # Display chat history
    st.subheader("Conversation")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Type your response here")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Build prompt
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert-powered supply chain demand forecaster."),
            ("human", user_input)
        ])

        # Generate response
        st.subheader("Generating Response...")
        with st.spinner("Thinking..."):
            try:
                conversation_chain = prompt_template | llm
                response = conversation_chain.invoke({"user_input": user_input})
                assistant_response = response.get("text", "Sorry, I couldn’t understand that.")
            except Exception as e:
                assistant_response = f"An error occurred: {e}"

        # Save and display response
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

# Add a reset button
if st.sidebar.button("Reset Chat"):
    st.session_state.clear()
    st.experimental_rerun()

st.sidebar.info("Built with ❤️ using Streamlit and LangChain")

# Let me know if you want to refine this or add new features! 🚀
