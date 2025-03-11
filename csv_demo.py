from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser

import os
import streamlit as st


def main():

    # Load the OpenAI API key from the



    csv_file = st.file_uploader("Upload a CSV file", type="csv")
    if csv_file is not None:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-pro-exp-02-05", temperature=0)

        agent = create_csv_agent(
            llm, csv_file, verbose=True,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,allow_dangerous_code=True
)
        
        user_question = "Generate a report in JSON format that details the quantity of sales broken down by month and by product. The report should include monthly totals for each product."

        if user_question is not None and user_question != "":
            with st.spinner(text="In progress..."):
                answer = agent.run(user_question)
                st.write(answer)


if __name__ == "__main__":
    main()