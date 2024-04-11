import os
import textwrap
import pandas as pd
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
from langchain_google_vertexai import  ChatVertexAI
from dotenv import load_dotenv
import time


# start timer
start_time = time.time()
# Function to print responses in a formatted way
def print_response(response: str):
    print("\n".join(textwrap.wrap(response, width=100)))

# Initialize environment and model
load_dotenv()
# model = model = ChatOpenAI(model='gpt-4-turbo', temperature=0)
model = ChatVertexAI( model_name="gemini-pro", temperature=0, convert_system_message_to_human=True)

# Load the dataset
df = pd.read_csv('/Users/mikeparsons/Documents/code/misc_projects_2/agents/metadata_agent/5G_Data_Sample.csv')  # Update this with your actual CSV file path


def create_report_step(model, template_str, input_variables):
    """Function to create a step for the report."""
    prompt_template = PromptTemplate(
        input_variables=input_variables,
        template=template_str
    )
    return LLMChain(llm=model, prompt=prompt_template, verbose=True)

# Define the prompt templates for generating different parts of the metadata report
templates = {
    "dataset_info": "Generate a high-level overview of the dataset based on the following info: {dataset_info}",
    "column_info": "Provide detailed metadata for each column based on the following info: {column_info}",
    "data_lineage": "Generate a hypothetical data lineage diagram for the dataset in Mermaid diagram syntax. Assume a simple ETL process from CSV files in GCS to BigQuery.",
    "airflow_etl_pipeline": "Generate an outline for an Airflow DAG that automates an ETL pipeline transferring data from CSV files in Google Cloud Storage to Google BigQuery. The pipeline should be scheduled to run daily, process data covering the past year, perform data transformation using SQL queries, include steps for checking data quality such as verifying there are no null values in essential columns, track data lineage, and implement monitoring and alerting mechanisms for data quality issues.",
    "airflow_etl_code": "Provide a Python code snippet for an Apache Airflow DAG that automates the ETL process from CSV files in GCS to a BigQuery table. Consider the following specifications: DAG ID: `csv_to_bigquery_etl`, schedule: Daily at midnight UTC, default arguments: Retries 3 times with a 5-minute delay, Task 1: `load_csv_to_bigquery` - Loads CSV data from GCS to a BigQuery staging table using the `GoogleCloudStorageToBigQueryOperator`, Task 2: `transform_data` - Applies SQL transformations on the staging table and inserts the results into the final table, Task 3: `data_quality_check` - Checks for nulls in key columns using the `BigQueryCheckOperator`, Task 4: `alert_on_failure` - Sends an alert if any task fails. Include necessary imports, default arguments, and the DAG definition. Assume that connection IDs for GCS and BigQuery are 'google_cloud_default'.",
    "data_usage": "crate a markdown diagram of what the data linage would look like",
    "data_access_permissions": "Describe who might have access to the data in a typical organization and at what level (read, write, admin). Include any common restrictions or privacy considerations.",
    "data_quality_metrics": "Outline potential data validation rules, consistency checks, and data quality metrics such as completeness, uniqueness, and accuracy. Note any common data quality issues.",
    "performance_metrics": "Discuss typical performance metrics for BigQuery datasets, such as query performance and data refresh rates. Mention hypothetical indexing and partitioning strategies for optimization.",
    "cost_management": "Explain the cost associated with storing and querying data in BigQuery and provide tips for cost optimization, assuming the dataset's storage in BigQuery.",
    "version_control": "Describe a hypothetical version control approach for the dataset and SQL scripts, considering common practices such as using Git.",
    "data_refresh_schedules": "Detail a typical ETL job schedule for refreshing the dataset, including refresh frequencies and the last updated timestamp.",
    "change_management": "Outline a change management process for the dataset, including schema changes or data updates, with a hypothetical link to a change request form or tracking system.",
    "business_context": "Provide a hypothetical business context for the dataset, detailing its relevance to business processes, decision-making, and key performance indicators.",
    "compliance_security": "Discuss compliance and security measures for the dataset, considering common data governance policies and security practices.",
    "recommendations": "Offer suggestions for potential improvements or optimizations to the dataset or ETL process, considering upcoming changes or enhancements."
}

# Define the LLM chains for each part of the report using the create_report_step function
report_steps = {name: create_report_step(model, template, [name])
                for name, template in templates.items()}


def run_report_steps(report_steps, info):
    """Function to run all report steps and collect their outputs."""
    outputs = {}
    for name, chain in report_steps.items():
        response = chain.invoke({name: info[name]})
        print(f"Raw response for {name}: {response}")  # Debug: print the raw response
        if 'text' in response:  # Use 'text' key to extract content
            outputs[name] = response['text']
        else:
            print(f"Unexpected response structure for {name}: {response}")  # Debug: print a warning message
            outputs[name] = ""  # Handle unexpected structure by setting a default value
    return outputs

# Generate dataset information as inputs for the chains
info = {
    "dataset_info": f"The dataset contains {len(df)} rows and {len(df.columns)} columns named {', '.join(df.columns)}.",
    "column_info": ", ".join(df.columns.tolist()),
    "data_lineage": "Placeholder for data lineage information.",  # Add this line
    # Add placeholders or initial content for any other keys needed, based on your templates
    "airflow_etl_pipeline": "Placeholder for Airflow ETL pipeline description.",
    "airflow_etl_code": "Placeholder for Airflow ETL code snippet.",
    "data_usage": "Placeholder for data usage information.",
    "data_access_permissions": "Placeholder for data access and permissions information.",
    "data_quality_metrics": "Placeholder for data quality metrics.",
    "performance_metrics": "Placeholder for performance metrics.",
    "cost_management": "Placeholder for cost management information.",
    "version_control": "Placeholder for version control information.",
    "data_refresh_schedules": "Placeholder for data refresh schedules.",
    "change_management": "Placeholder for change management process.",
    "business_context": "Placeholder for business context.",
    "compliance_security": "Placeholder for compliance and security information.",
    "recommendations": "Placeholder for recommendations."
}

# Run all report steps
outputs = run_report_steps(report_steps, info)

def generate_final_report(outputs):
    """Function to generate the final report using markdown format."""
    final_report = "# Final Metadata Report\n\n"
    
    # Dynamically add sections based on 'outputs'
    for section_name, content in outputs.items():
        section_header = section_name.replace("_", " ").title()
        final_report += f"## {section_header}\n{content}\n\n"
    
    final_report += "*This report is generated in markdown format for better readability.*\n"
    
    return final_report

# Generate the final report
final_report = generate_final_report(outputs)

# Save the report to a markdown file
with open("metadata_report.md", "w") as file:
    file.write(final_report)


# end timer 
end_time = time.time()
total_time_seconds = end_time - start_time

# Convert seconds to minutes
total_time_minutes = total_time_seconds / 60
print(total_time_minutes)
print(f"Total time taken: {total_time_seconds:.2f} seconds ({total_time_minutes:.2f} minutes).")