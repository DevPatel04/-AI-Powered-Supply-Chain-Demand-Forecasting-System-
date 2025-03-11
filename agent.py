from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI

def get_sales_report(csv_path):
    if csv_path is not None:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-pro-exp-02-05", temperature=0)

        agent = create_csv_agent(
            llm, csv_path, verbose=True,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,allow_dangerous_code=True
)
        
        user_question = "Generate a report in JSON format that details the quantity of sales broken down by month and by product. The report should include monthly totals for each product."

        if user_question is not None and user_question != "":
            answer = agent.run(user_question)
            return answer

