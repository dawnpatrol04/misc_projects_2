import pandas as pd
import json
import matplotlib.pyplot as plt
from langchain_openai import OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_vertexai import  ChatVertexAI
from langchain_openai import ChatOpenAI
import pandas as pd
from dotenv import load_dotenv 
import json
import matplotlib.pyplot as plt


load_dotenv()
# llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
llm = ChatVertexAI( model_name="gemini-pro", temperature=0, convert_system_message_to_human=True)

def csv_tool(filename : str):
    df = pd.read_csv(filename)
    return create_pandas_dataframe_agent(llm=llm, df=df, verbose=True)
    
   

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
        You are working with a pandas DataFrame containing a dataset with various attributes. Your task is to identify anomalies or outliers in this data, leveraging your Python and pandas skills. Keep in mind that the data might not always follow a normal distribution, and you should choose the anomaly detection method accordingly.

        Here's a structured approach to guide you:

        1. Explore the Data:
        - Display the first few rows to understand the structure:
            `print(df.head())`
        - Summarize statistical properties to get an overview:
            `print(df.describe())`
        - Plot a histogram or a box plot for the column of interest to understand its distribution:
            `df['column_of_interest'].hist()` or `df.boxplot(column=['column_of_interest'])`

        2. Clean the Data:
        - If there are missing values, handle them appropriately. For example, you might choose to fill them with the median value of the column:
            `df[column].fillna(df[column].median(), inplace=True)`

        3. Select the Right Method for Anomaly Detection:
        - If the data appears to be normally distributed, consider using the Z-score method to detect anomalies. Values beyond 3 or -3 standard deviations from the mean can be considered outliers.
        - For skewed data or when the distribution is not normal, use the Interquartile Range (IQR) method. Data points outside 1.5 * IQR from the first and third quartiles are typically considered outliers.

        4. Detect and Report Anomalies:
        - For the Z-score method:
            ```
            from scipy import stats
            z_scores = stats.zscore(df['column_of_interest'])
            df['is_anomaly'] = np.abs(z_scores) > 3
            ```
        - For the IQR method:
            ```
            Q1 = df['column_of_interest'].quantile(0.25)
            Q3 = df['column_of_interest'].quantile(0.75)
            IQR = Q3 - Q1
            df['is_anomaly'] = (df['column_of_interest'] < (Q1 - 1.5 * IQR)) | (df['column_of_interest'] > (Q3 + 1.5 * IQR))
            ```
        - Generate a report summarizing the anomalies detected and their distribution:
            ```
            anomalies = df[df['is_anomaly'] == True]
            print(f"Detected {len(anomalies)} anomalies.")
            print("Anomaly Summary:")
            print(anomalies.describe())
            ```

        Example Output for Anomaly Detection Report:
        Detected 15 anomalies.
        Anomaly Summary:
        column_of_interest ... is_anomaly
        count 15.000000 ... 15.0
        mean 123.456789 ... 1.0
        std 10.123456 ... 0.0
        min 110.000000 ... 1.0
        25% 115.000000 ... 1.0
        50% 120.000000 ... 1.0
        75% 130.000000 ... 1.0
        max 140.000000 ... 1.0

        sql
        Copy code

        This output indicates that 15 anomalies were detected in the 'column_of_interest' with various statistics describing these anomalous values.

        Identify anomalies in the "Bandwidth Capacity (Gbps)" column, considering its distribution and choosing the appropriate method for anomaly detection.
        """
        + query
    )

    # Run the prompt through the agent and capture the response.
    response = agent.invoke(prompt)

    # Return the response converted to a string.
    return str(response)


def decode_response(response: str) -> dict:
    return  response

if __name__ == "__main__":
    # Example usage with hardcoded values
    csv_file = '/Users/mikeparsons/Documents/code/misc_projects_2/agents/outlyer_detect/5G_Data_Sample.csv'  # Update this with your CSV file path
    query = 'Identify anomalies in the "Bandwidth Capacity (Gbps)" column.'  # Example query

    # Create an agent from the CSV file.
    agent = csv_tool(csv_file)
    # Query the agent.
    response = ask_agent(agent=agent, query=query)
    # Decode the response.
    decoded_response = decode_response(response)
    print("Agent's response:", decoded_response)
    # Here, you can further process the decoded_response as needed