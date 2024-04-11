import pandas as pd
import json
import matplotlib.pyplot as plt
from langchain_openai import OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

import os

# Replace 'your_openai_api_key' with your actual OpenAI API key
API_KEY =  os.environ.get('OPENAI_API_KEY')

def create_agent(filename):
    """
    Create an agent to analyze the CSV data using OpenAI's API.
    """
    llm = OpenAI(api_key=API_KEY)
    df = pd.read_csv(filename)
    return create_pandas_dataframe_agent(llm, df, verbose=True)

def query_agent(agent, query):
    """
    Query the agent and return the structured response.
    """
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

        Now, let's tackle the query step by step. Here's the query for you to work on: 
        """
        + query
    )
    response = agent.invoke(prompt)
    print(response)
    return json.loads(response) 

def generate_visualization(response):
    """
    Generate and save visualizations based on the agent's response.
    """
    if 'table' in response:
        table_data = response['table']
        df = pd.DataFrame(table_data['data'], columns=table_data['columns'])
        df.to_csv('output_table.csv', index=False)
        print("Table saved as 'output_table.csv'.")
    elif 'bar' in response:
        chart_data = response['bar']
        df = pd.DataFrame([chart_data['data']], columns=chart_data['columns'])
        df.plot(kind='bar')
        plt.savefig('bar_chart.png')
        print("Bar chart saved as 'bar_chart.png'.")
    elif 'line' in response:
        chart_data = response['line']
        df = pd.DataFrame([chart_data['data']], columns=chart_data['columns'])
        df.plot()
        plt.savefig('line_chart.png')
        print("Line chart saved as 'line_chart.png'.")
    else:
        print("No recognizable visualization data found in the response.")

def main(csv_file, query):
    """
    Main function to read CSV, create an agent, query it, and generate visualizations.
    """
    agent = create_agent(csv_file)
    response = query_agent(agent, query)
    # print(response)
    generate_visualization(response)

if __name__ == "__main__":
    # Example usage with hardcoded values
    csv_file = '5G_Data_Sample.csv'  # Update this with your CSV file path
    query = 'craet a bar chat showing the Bandwidth Capacity (Gbps) by tower'  # Update this with your desired query
    main(csv_file, query)
