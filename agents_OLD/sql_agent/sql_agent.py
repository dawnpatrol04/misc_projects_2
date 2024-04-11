# langchain_sql_agent.py

# Import necessary libraries
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()

# Initialize the SQL Database connection
db = SQLDatabase.from_uri("sqlite:////Users/mikeparsons/Documents/code/misc_projects_2/agents/sql_agent/5G_Data_Sample.sqlite")

# Initialize the language model
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

# Create the SQL agent with the database and language model
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

# Define a function to invoke the agent with a human-readable prompt
def run_query(prompt):
    return agent_executor.invoke(prompt)

# Example usage
if __name__ == "__main__":
    prompt = "show me the tables in the sqlite database"
    result = run_query(prompt)
    print(result)
