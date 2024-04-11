from fastapi import FastAPI
import uvicorn
from typing import Optional

# Import the necessary functions from each agent's Python file
from agents.anomaly.anomaly_example import run_anomaly_detection
from agents.confluence.confluence_loader import load_confluence_data
from agents.data_viz.agent_pandasViz import generate_visualization
from agents.metadata.meta_agent import extract_metadata
from agents.sql_agent.sql_agent import run_sql_query

app = FastAPI()

# Define route for anomaly detection
@app.get("/anomaly")
def anomaly():
    # This should call the function from anomaly_example.py
    result = run_anomaly_detection()
    return result

# Define route for confluence data loading
@app.get("/confluence")
def confluence():
    # This should call the function from confluence_loader.py
    result = load_confluence_data()
    return result

# Define route for data visualization
@app.get("/data-viz/{chart_type}")
def data_viz(chart_type: str):
    # This should call the function from agent_pandasViz.py
    # Assuming the function takes a chart type as a parameter
    result = generate_visualization(chart_type)
    return result

# Define route for metadata extraction
@app.get("/metadata")
def metadata():
    # This should call the function from meta_agent.py
    result = extract_metadata()
    return result

# Define route for SQL operations
@app.get("/sql-agent")
def sql_agent(query: Optional[str] = None):
    # This should call the function from sql_agent.py
    # Assuming the function takes an SQL query as a parameter
    result = run_sql_query(query)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
