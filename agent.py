from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import streamlit as st
import pandas as pd
import calendar as cal
def get_sales_report(csv_path):

    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY3"]
    """This function generates a sales report based on the provided CSV file."""
    if csv_path is not None:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-pro-exp-02-05", temperature=0)

        # llm = ChatGroq(model="llama3-70b-8192", temperature=0)
        
        agent = create_csv_agent(
            llm, csv_path, verbose=True,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,allow_dangerous_code=True)
        
        user_question = "Generate a report in proper format that details the quantity of sales broken down by month and by product. The report should include monthly totals for each product."
        
        if user_question is not None and user_question != "":
            answer = agent.run(user_question)
            print(answer)
            return answer

