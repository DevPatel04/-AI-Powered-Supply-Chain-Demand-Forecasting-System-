import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure secrets and page settings
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
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
else: 
    user_input =  st.chat_input("Type your response here")

    


if submit_button:
    st.session_state.input_data_set = True
    # Display input summary
    st.subheader("Input Summary")
    st.markdown(f"**Industry:** {industry}")
    st.markdown(f"**Products/Services:** {products}")
    st.markdown(f"**Location:** {location}")
    st.markdown(f"**Data Constraints:** {data_constraints}")
    st.markdown(f"**Timeframe:** {timeframe}")

    # Build the prompt for the LLM
    prompt = f"""
**Context:**

- **Industry:** {industry}
- **Products/Services:** {products}
- **Location:** {location}
- **Data:** {data_constraints}
- **Timeframe:** {timeframe}

**Task:**

Act as an expert demand forecaster and supply chain strategist for the given industry. Create a detailed stock/resource list for the business operating in the specified location within the defined timeframe, considering the constraints of available data.

**Instructions:**

1. **Stock/Resource List:**
   - Provide a detailed list with specific quantities for each primary category and its subcategories.
   - Include total numbers and breakdowns.

2. **Festival/Seasonal/Event Analysis:**
   - Identify major festivals, seasons, or events within the timeframe.
   - Analyze their impact on demand for each category and explain which items/services surge and why.

3. **Market Trends:**
   - Incorporate relevant market trends that influence consumer behavior in the specified industry and location.

4. **Assumptions:**
   - Clearly state all assumptions used in your forecast (e.g., estimated population, market penetration, etc.) with logical reasoning.

5. **Stock/Resource Management Strategy:**
   - Recommend an approach for stock/resource management given the lack of historical data.
   - Include initial stock, restocking schedules (especially before festivals), and shelf-life management.

**Output Format:**

- Use markdown with headings, bullet points, and tables.
- Provide numerical data for all items.
- Include a summary table of the final stock/resource list.
"""
    
    

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert powered supply chain demand forecaster."),
        ("human", prompt)
    ])

    st.subheader("Generating Response...")

    try:
        conversation_chain = prompt_template | llm

        # Use invoke method to get the response from the LLM
        response = conversation_chain.invoke({"user_input": prompt})

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
