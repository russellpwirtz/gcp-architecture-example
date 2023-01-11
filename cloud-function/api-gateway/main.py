from flask import jsonify, Response
import time
import json
from google.cloud import workflows_v1beta
from google.cloud.workflows import executions_v1beta
from google.cloud.workflows.executions_v1beta.types import executions

def adjustments_gateway(request) -> Response:
    project = 'spanner-demo-369019'
    location = 'us-west2'
    workflow = 'adjustmentsWorkflow'
    return execute_workflow(request, project, location, workflow)

def execute_workflow(request, project, location, workflow):
    if not project:
        raise Exception('project is required.')

    # Set up API clients.
    execution_client = executions_v1beta.ExecutionsClient()
    workflows_client = workflows_v1beta.WorkflowsClient()
    print(f"Got api gateway request - {str(request.get_json())}")

    parent = workflows_client.workflow_path(project, location, workflow)
    response = execution_client.create_execution(parent=parent, execution=executions.Execution(argument=json.dumps(request.get_json())))
    print(f"Created execution: {response.name}")

    execution_finished = False
    backoff_delay = 0.1
    print('Poll for result...')
    while (not execution_finished):
        execution = execution_client.get_execution(request={"name": response.name})
        execution_finished = execution.state != executions.Execution.State.ACTIVE

        # If we haven't seen the result yet
        if not execution_finished:
            print('- Waiting for results...')
            time.sleep(backoff_delay/10)
            backoff_delay *= 2  # Double the delay to provide exponential backoff.
        else:
            print(f'Execution finished with state: {execution.state.name}')
            print(execution.result)
            return execution.result


