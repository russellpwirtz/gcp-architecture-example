from flask import Response
import json
from google.cloud import workflows_v1beta
from google.cloud.workflows import executions_v1beta
from google.cloud.workflows.executions_v1beta.types import executions
from dotenv import load_dotenv
load_dotenv()
import os

# requires .env file
GCP_PROJECT: str = os.getenv("GCP_PROJECT")
GCP_REGION: str = os.getenv("GCP_REGION")

IP_ADDRESS_HEADER: str = 'X-Forwarded-For'
ORIGINAL_PATH_HEADER: str = 'X-Envoy-Original-Path'

def workflow_gateway(request) -> Response:
    ip_address = request.headers.get(IP_ADDRESS_HEADER)
    method = request.method.lower()
    api_path = request.headers.get(ORIGINAL_PATH_HEADER).split("?")[0] if "?" in request.headers.get(ORIGINAL_PATH_HEADER) else request.headers.get(ORIGINAL_PATH_HEADER)
    workflow = method + "-" + api_path.replace('/','') + "-workflow"

    print(f"API request from IP: {ip_address} for path: {api_path}, method: {method}, workflow: {workflow}")

    return execute_workflow(request, workflow)

def execute_workflow(request, workflow) -> Response:
    if not GCP_PROJECT:
        raise Exception('project is required.')

    execution_client = executions_v1beta.ExecutionsClient()
    workflows_client = workflows_v1beta.WorkflowsClient()

    parent = workflows_client.workflow_path(GCP_PROJECT, GCP_REGION, workflow)

    workflow_params = request.get_json()
    workflow_params['gcp_project'] = GCP_PROJECT
    workflow_params['gcp_region'] = GCP_REGION

    response = execution_client.create_execution(parent=parent, 
        execution=executions.Execution(argument=json.dumps(workflow_params)))
    
    execution_id = response.name.split("/executions/")[1]
    
    print(f"Created execution id: {execution_id} with name {response.name}")

    return {"job_id": execution_id}, 200


