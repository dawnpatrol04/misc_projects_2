import os
import pandas as pd
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_vertexai import ChatVertexAI
from dotenv import load_dotenv
import time

def initialize_model():
    load_dotenv()
    model = ChatVertexAI(model_name="gemini-pro", temperature=0, top_p=0, project='vz-nonit-np-jaov-dev-fpasdo-0', convert_system_message_to_human=True )
    return model

def load_dataset(filepath):
    return pd.read_csv(filepath)

def create_report_step(model, template_str, input_variable):
    prompt_template = PromptTemplate(input_variables=[input_variable], template=template_str)
    return LLMChain(llm=model, prompt=prompt_template, verbose=True)

def generate_report_steps(model):
    templates = {
    "dataset_info": "Generate a high-level overview of the dataset based on the following info: {dataset_info}",
    "column_info": "Provide detailed metadata for each column based on the following info: {column_info}",
    "data_lineage": "Generate a hypothetical data lineage diagram for the dataset in Mermaid diagram syntax. Assume a simple ETL process from CSV files in GCS to BigQuery.",
    "airflow_etl_pipeline": "Generate an outline for an Airflow DAG that automates an ETL pipeline transferring data from CSV files in Google Cloud Storage to Google BigQuery. The pipeline should be scheduled to run daily, process data covering the past year, perform data transformation using SQL queries, include steps for checking data quality such as verifying there are no null values in essential columns, track data lineage, and implement monitoring and alerting mechanisms for data quality issues.",
    "airflow_etl_code": "Provide a Python code snippet for an Apache Airflow DAG that automates the ETL process from CSV files in GCS to a BigQuery table. Consider the following specifications: DAG ID: `csv_to_bigquery_etl`, schedule: Daily at midnight UTC, default arguments: Retries 3 times with a 5-minute delay, Task 1: `load_csv_to_bigquery` - Loads CSV data from GCS to a BigQuery staging table using the `GoogleCloudStorageToBigQueryOperator`, Task 2: `transform_data` - Applies SQL transformations on the staging table and inserts the results into the final table, Task 3: `data_quality_check` - Checks for nulls in key columns using the `BigQueryCheckOperator`, Task 4: `alert_on_failure` - Sends an alert if any task fails. Include necessary imports, default arguments, and the DAG definition. Assume that connection IDs for GCS and BigQuery are 'google_cloud_default'.",
    "data_usage": "show code examples of how to use this table : python , sql , javascript",
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
    return {name: create_report_step(model, template, name) for name, template in templates.items()}

def run_report_steps(report_steps, df):
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

    outputs = {}
    for name, chain in report_steps.items():
        response = chain.invoke({name: info[name]})
        outputs[name] = response.get('text', "")
    return outputs

def generate_final_report(outputs):
    final_report = "# Final Metadata Report\n\n"
    for section_name, content in outputs.items():
        section_header = section_name.replace("_", " ").title()
        final_report += f"## {section_header}\n{content}\n\n"
    final_report += "*This report is generated in markdown format for better readability.*\n"
    return final_report

def save_report(report, filename):
    with open(filename, "w") as file:
        file.write(report)

def process_report(csv_filepath, output_filename):
    start_time = time.time()

    model = initialize_model()
    df = load_dataset(csv_filepath)
    report_steps = generate_report_steps(model)
    outputs = run_report_steps(report_steps, df)
    final_report = generate_final_report(outputs)
    save_report(final_report, output_filename)

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    csv_filepath = '/Users/V721215/Code/hackathon_prez/Salck_bot/agents/metadata_agent/5G_Data_Sample.csv'  # Update this path
    output_filename = "metadata_report_2.md"
    process_report(csv_filepath, output_filename)
