from fastapi import FastAPI, Query
from eclipse_agent import EclipseAgentWorkflow
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from dotenv import load_dotenv
import os

load_dotenv()

workflow = EclipseAgentWorkflow(
    session_id="eclipse_agent_session",
    storage=SqlWorkflowStorage(
        table_name="eclipse_agent_workflows",
        db_file="eclipse_agent_workflows.db",
    ),
)

app = FastAPI()


@app.post("/query/")
def query_endpoint(query: str =Query(..., description="Your query about Eclipse")):
    responses = []
    for response in workflow.run(query):
        responses.append(response.content)
    return {"response": responses}
