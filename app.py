import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
st.title("Website Maker Chatbot")

if "chat_history_architecture" not in st.session_state:
    st.session_state.chat_history_architecture = []

if "input_data" not in st.session_state:
    st.session_state.input_data = {
        "industry": "Retail",
        "products": "Chocolates, Gift Items, Sweets",
        "location": "Mumbai, India",
        "data": "Limited historical sales data, focus on festival-driven demand",
        "timeframe": "March 2025 - May 2025"
    }

if "current_step" not in st.session_state:
    st.session_state.current_step = 0

# Sidebar for navigation
st.sidebar.title("Navigation")
model_name = st.sidebar.selectbox("Select Model", ["llama-3.1-8b-instant", "gemini-2.0-pro-exp-02-05" ,"gemini-2.0-flash-thinking-exp-01-21"])

if model_name == "llama-3.1-8b-instant":
    llm = ChatGroq(
        model=model_name,
        temperature=0.5,
    )
elif model_name == "gemini-2.0-pro-exp-02-05" or model_name == "gemini-2.0-flash-thinking-exp-01-21":
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.5,
    )

st.header("Architecture")

# Steps to collect inputs
steps = [
    "Enter the industry:",
    "Enter the products/services:",
    "Enter the location:",
    "Enter the data constraints:",
    "Enter the timeframe:"
]

# Display the current step prompt
if st.session_state.current_step < len(steps):
    if st.session_state.input_data[list(st.session_state.input_data.keys())[st.session_state.current_step]]:
        with st.chat_message("assistant"):
            st.markdown(f"**{steps[st.session_state.current_step]}** {st.session_state.input_data[list(st.session_state.input_data.keys())[st.session_state.current_step]]}")
        st.session_state.current_step += 1
    else:
        with st.chat_message("assistant"):
            st.markdown(steps[st.session_state.current_step])

user_input = st.chat_input("Type your response here")

if user_input:
    # Store the input in session state
    if st.session_state.current_step == 0:
        st.session_state.input_data["industry"] = user_input
    elif st.session_state.current_step == 1:
        st.session_state.input_data["products"] = user_input
    elif st.session_state.current_step == 2:
        st.session_state.input_data["location"] = user_input
    elif st.session_state.current_step == 3:
        st.session_state.input_data["data"] = user_input
    elif st.session_state.current_step == 4:
        st.session_state.input_data["timeframe"] = user_input

    # Display the user's input as a chat message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Move to the next step
    st.session_state.current_step += 1

    # If all inputs are collected, proceed with generating the response
    if st.session_state.current_step >= len(steps):
        prompt = """Context:

Industry: {industry}
Products/Services: {products}
Location: {location}
Data: {data}
Timeframe: {timeframe}
Task:

Act as an expert demand forecaster and supply chain strategist for the given industry. Your task is to create a detailed stock list (or resource allocation plan) for the business operating in the specified location within the defined timeframe, considering the constraints of available data.

Instructions:

Stock/Resource List:

Provide a detailed list with specific quantities for each primary category and its subcategories.
Example for Product-Based Businesses:
Main Category 1: [e.g., Chocolates]
Subcategory A: [e.g., Milk Bars]
Subcategory B: [e.g., Dark Bars]
Subcategory C: [e.g., Assorted Boxes]
Subcategory D: [e.g., Premium Selection]
Main Category 2: [e.g., Gift Items]
Subcategory A: [e.g., Hampers]
Subcategory B: [e.g., Decorative Items]
Subcategory C: [e.g., Personalized Gifts]
Main Category 3: [e.g., Sweets]
Subcategory A: [e.g., Traditional]
Subcategory B: [e.g., Baked]
Subcategory C: [e.g., Sugar-Free]
For service-based or other industries, adjust the categories accordingly.
Include total numbers and detailed breakdowns.
Festival/Seasonal/Event Analysis:

Identify any major festivals, seasons, or events within the specified timeframe.
Analyze their impact on demand for each category. Explain which items or services will see a surge and why.
Example: “Festivals such as Holi boost demand for sweets and gift items as consumers are inclined toward celebratory purchases.”
Market Trends:

Incorporate relevant market trends that influence consumer behavior in the specified industry and location.
Examples:
Growth trends in product segments (e.g., the rising premium chocolate market)
Cultural or seasonal shifts in consumer preferences
Regional factors affecting demand
Assumptions:

Clearly state all assumptions used in your forecast (e.g., estimated population size, market penetration rate, sales distribution assumptions).
Provide logical reasoning or industry insights to justify each assumption.
Stock/Resource Management Strategy:

Recommend a management approach to deal with the lack of historical data.
Include guidelines for:
Initial stock or resource allocation levels
A restocking or resource replenishment schedule (especially before major events)
Managing shelf-life or service capacities to minimize waste or downtime
Output Format:

Use markdown with headings, bullet points, and tables for clarity.
Provide numerical data for all stock or resource items.
Include a summary table of the final stock/resource list.
Example Output:

Festival/Seasonal Analysis:
“Festivals such as Holi, Ugadi, Ram Navami, and Akshaya Tritiya drive an increase in demand for sweets and gift items due to their cultural significance and gifting practices.”

Stock/Resource List:

Category	Total Units	Breakdown
Chocolates	5,000	Milk Bars: 2,000, Dark Bars: 1,000, Assorted Boxes: 1,000, Premium: 1,000
Gift Items	3,000	Hampers: 1,500, Decorative Items: 1,000, Personalized: 500
Sweets	4,000	Traditional: 2,000, Baked: 1,000, Sugar-Free: 1,000
Strategy:
“Initiate with 50% of the forecasted demand as the initial order. Monitor sales daily and adjust restocking frequencies, especially prior to identified festivals. Ensure proper shelf-life management to reduce product wastage and optimize storage logistics.”"""

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert powered supply chain demand forecstaster"),
            ("human", prompt.format(**st.session_state.input_data))
        ])

        st.session_state.conversation_chain = prompt_template | llm

        st.session_state.chat_history_architecture.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("assistant"):
            try:
                response = st.session_state.conversation_chain.invoke({"user_input": user_input, **st.session_state.input_data})
                assistant_response = response.content if response else "Sorry, I couldn’t understand that."
            except Exception as e:
                assistant_response = f"An error occurred: {e}"

            st.markdown(assistant_response)

            st.session_state.chat_history_architecture.append({
                "role": "assistant",
                "content": assistant_response
            })

        # Reset the current step for the next interaction
        st.session_state.current_step = 0
