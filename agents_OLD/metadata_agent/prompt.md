 "dataset_info": "Generate a high-level overview of the dataset based on the following info: {dataset_info}",
    "column_info": "Provide detailed metadata for each column based on the following info: {column_info}",
    "data_lineage": "Generate a hypothetical data lineage diagram for the dataset in Mermaid diagram syntax. Assume a simple ETL process from CSV files in GCS to BigQuery.",
    "data_usage": "Summarize how the data has been used historically, including common queries and critical reports. Provide hypothetical examples of BigQuery queries and visualization tools such as Python, Qlik, and Tableau.",
    "data_access_permissions": "Describe who might have access to the data in a typical organization and at what level (read, write, admin). Include any common restrictions or privacy considerations.",
    "performance_metrics": "Discuss typical performance metrics for BigQuery datasets, such as query performance and data refresh rates. Mention hypothetical indexing and partitioning strategies for optimization.",
    "data_quality_metrics": "Outline potential data validation rules, consistency checks, and data quality metrics such as completeness, uniqueness, and accuracy. Note any common data quality issues.",
    "cost_management": "Explain the cost associated with storing and querying data in BigQuery and provide tips for cost optimization, assuming the dataset's storage in BigQuery.",
    "version_control": "Describe a hypothetical version control approach for the dataset and SQL scripts, considering common practices such as using Git.",
    "data_refresh_schedules": "Detail a typical ETL job schedule for refreshing the dataset, including refresh frequencies and the last updated timestamp.",
    "change_management": "Outline a change management process for the dataset, including schema changes or data updates, with a hypothetical link to a change request form or tracking system.",
    "business_context": "Provide a hypothetical business context for the dataset, detailing its relevance to business processes, decision-making, and key performance indicators.",
    "compliance_security": "Discuss compliance and security measures for the dataset, considering common data governance policies and security practices.",
    "recommendations": "Offer suggestions for potential improvements or optimizations to the dataset or ETL process, considering upcoming changes or enhancements."
    "airflow_etl_pipeline": """
    Generate an outline for an Airflow DAG that automates an ETL pipeline transferring data from CSV files in Google Cloud Storage to Google BigQuery. The pipeline should:

    - Be scheduled to run daily.
    - Process data covering the past year.
    - Perform data transformation using SQL queries.
    - Include steps for checking data quality, such as verifying there are no null values in essential columns.
    - Track data lineage.
    - Implement monitoring and alerting mechanisms for data quality issues.
  "airflow_etl_code": """
    Provide a Python code snippet for an Apache Airflow DAG that automates the ETL process from CSV files in GCS to a BigQuery table. Consider the following specifications:

    - DAG ID: `csv_to_bigquery_etl`
    - Schedule: Daily at midnight UTC.
    - Default arguments: Retries 3 times with a 5-minute delay.
    - Task 1: `load_csv_to_bigquery` - Loads CSV data from GCS to a BigQuery staging table using the `GoogleCloudStorageToBigQueryOperator`.
    - Task 2: `transform_data` - Applies SQL transformations on the staging table and inserts the results into the final table.
    - Task 3: `data_quality_check` - Checks for nulls in key columns using the `BigQueryCheckOperator`.
    - Task 4: `alert_on_failure` - Sends an alert if any task fails.

    Include necessary imports, default arguments, and the DAG definition. Assume that connection IDs for GCS and BigQuery are 'google_cloud_default'.
