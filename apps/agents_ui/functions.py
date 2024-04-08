from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_google_vertexai import VertexAI


def slack_assistant(user_input, model_name="gemini-pro", temperature=0.7):
    """
    Creates a Slack assistant using a language model from Vertex AI.

    Parameters:
    - user_input (str): The query or request from the user.
    - model_name (str): The name of the model to use from Vertex AI.
    - temperature (float): The creativity of the model's responses.

    Returns:
    - str: The assistant's response to the user input.
    """

    # Initialize the chat model with Vertex AI
    chat = VertexAI(model_name=model_name, temperature=temperature)

    # System message template describing the assistant's capabilities and behavior
    system_template = """
    You are an intelligent Slack assistant designed to help users with various tasks,
    answer questions, and provide information as needed within a Slack environment.

    Your goal is to understand the user's request and provide a concise, helpful response.
    Be friendly and professional in your tone, aiming to facilitate productivity and
    collaboration within the team.

    Respond directly to the user's query, offering solutions, information, or performing tasks
    as requested. Use clear and straightforward language to ensure your assistance is easily
    understood.

    Start your response by addressing the user by name, then proceed with your assistance.
    For example: "Hi, sure, I can help with that. Here's what I found...".
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template.strip())

    # Human message template for capturing user input
    human_template = "User's query or request for assistance: {user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # Combine the system and human prompts into a chat prompt
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Execute the chat model with the given prompts
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.invoke(input=user_input)

    return response
