from dotenv import load_dotenv
import os
import requests
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
from langchain_community.utilities.jira import JiraAPIWrapper
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


from langchain_google_vertexai import VertexAI
from langchain_google_vertexai import  ChatVertexAI


load_dotenv()

# Retrieve environment variables
jira_token = os.getenv('JIRA_API_TOKEN')
jira_email = os.getenv('JIRA_USERNAME')
jira_url = os.getenv('JIRA_URL')
openai_api_key = os.getenv('OPENAI_API_KEY')
jira_instance_url = os.getenv('JIRA_URL')

def agents(user_input):

    llm = ChatVertexAI( model_name="gemini-pro", temperature=0.7)


    jira = JiraAPIWrapper(jira_instance_url=jira_instance_url, jira_username=jira_email, jira_api_token=jira_token)
    toolkit = JiraToolkit.from_jira_api_wrapper(jira)
    tools = toolkit.get_tools()
    

    # Your prompt template with the current date and time included
    template = f"""
        You are an AI assistant with the following capabilities:

        1. **Creating JIRA Tickets:**
        - **Project Keys:** Use "PROD" 
        - **Issue Types:** "Tasks," "Bugs," or "Requests."
        - **Priority:** "Lowest," "Low," "Medium" (default), "High," or "Highest."

        To create a ticket, the instruction will start with "Create Ticket:" followed by the details in the format "[Summary], [Description (optional)], [Priority (optional)]."

        2. **Retrieving Information:**
        - You can also retrieve and display information about existing JIRA items.

        For retrieval, the instruction will start with "Retrieve:" followed by the specifics of the request, like "open Tasks" or "High priority Bugs."
        
        3. **Changing Ticket Status:**
        -  You can change the status of JIRA issues to reflect their current stage in the workflow. The Kanban board has three columns: "TO DO," "IN PROGRESS," and "DONE."


        To change a ticket's status, the instruction will mention update, change, or modify followed by the ticket number and the new status 

        **Your Task:**
        - Based on the above instructions and the input provided, determine whether to create a ticket or retrieve information.
        - For creation, ensure all required fields are filled. If the description is missing, craft a suitable one.
        - For retrieval, clearly list the requested items without creating a new ticket.
        - Works like pull , get , fetch , show , list , display , etc for retrieval.
        **Input Received:** "{{input}}"

            
    """

    _prompt = PromptTemplate(
    input_variables=["input"],
    template=template
    )
    prompt = _prompt.format(input=user_input)

    agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
    )
    response = agent.invoke(prompt)
    return str(response['output'])

   