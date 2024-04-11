import pandas as pd
import json
import matplotlib.pyplot as plt
from langchain_openai import OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_vertexai import  ChatVertexAI
import pandas as pd
from dotenv import load_dotenv 
import json
import matplotlib.pyplot as plt


load_dotenv()
llm = ChatVertexAI( model_name="gemini-pro", temperature=0, convert_system_message_to_human=True)

def csv_tool(filename : str):
    df = pd.read_csv(filename)
    return create_pandas_dataframe_agent(llm=llm, df=df)
    
   

def ask_agent(agent, query):
    """
    Query an agent and return the response as a string.

    Args:
        agent: The agent to query.
        query: The query to ask the agent.

    Returns:
        The response from the agent as a string.
    """
    # Prepare the prompt with query guidelines and formatting
    prompt = (
        """
        Let's decode the way to respond to the queries. The responses depend on the type of information requested in the query. 

        1. If the query requires a table, format your answer like this:
           {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

        2. For a bar chart, respond like this:
           {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

        3. If a line chart is more appropriate, your reply should look like this:
           {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

        Note: We only accommodate two types of charts: "bar" and "line".

        4. For a plain question that doesn't need a chart or table, your response should be:
           {"answer": "Your answer goes here"}

        For example:
           {"answer": "The Product with the highest Orders is '15143Exfo'"}

        5. If the answer is not known or available, respond with:
           {"answer": "I do not know."}

        Return all output as a string. Remember to encase all strings in the "columns" list and data list in double quotes. 
        For example: {"columns": ["Products", "Orders"], "data": [["51993Masc", 191], ["49631Foun", 152]]}

        before you start make sure the dataframe has the correct data types.

        Now, let's tackle the query step by step. Here's the query for you to work on: 
        """
        + query
    )

    # Run the prompt through the agent and capture the response.
    response = agent.invoke(prompt)

    # Return the response converted to a string.
    return str(response)

def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    return json.loads(response)

def write_answer(response_dict: dict):
    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        try:
            df_data = {
                col: [x[i] if isinstance(x, list) else x for x in data['data']]
                for i, col in enumerate(data['columns'])
            }
            df = pd.DataFrame(df_data)
            
            # Plotting the bar chart using matplotlib
            df.plot(kind='bar')
            plt.title('Bar Chart Representation')
            plt.xlabel('X-axis Label')
            plt.ylabel('Y-axis Label')
            
            # Saving the plot as an image file
            plt.savefig('bar_chart.png')
            print("Bar chart saved as 'bar_chart.png'.")
            
        except ValueError as e:
            print(f"Couldn't create DataFrame from data: {data}. Error: {e}")

if __name__ == "__main__":
    # Initialize attempt counter
    attempts = 0
    max_attempts = 5
    success = False

    # Example usage with hardcoded values
    csv_file = '/Users/mikeparsons/Documents/code/misc_projects_2/agents/data_viz/5G_Data_Sample.csv'  # Update this with your CSV file path
    query = ' bar chart: Bandwidth Capacity (Gbps) by Cell Tower ID'  # Update this with your desired query

    while attempts < max_attempts and not success:
        try:
            # Increment attempt counter
            attempts += 1

            # Create an agent from the CSV file.
            agent = csv_tool(csv_file)

            # Query the agent.
            response = ask_agent(agent=agent, query=query)

            # Decode the response.
            decoded_response = decode_response(response)

            # Write the response to the Streamlit app.
            write_answer(decoded_response)

            # If everything goes well, set success to True to break the loop
            success = True

        except Exception as e:
            # Print the error and the attempt number
            print(f"Attempt {attempts} failed with error: {e}")

            # If this was the last attempt, raise the error
            if attempts == max_attempts:
                raise

            # Optionally, you can add a short delay before the next attempt
            # import time
            # time.sleep(1)

    if success:
        print("Operation succeeded.")
    else:
        print("Operation failed after maximum attempts.")
