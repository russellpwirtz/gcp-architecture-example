# GCP Architecture example

Demo project for an event-driven serverless architecture in Google Cloud Platform

This project is an example of an event-driven serverless architecture on Google Cloud Platform (GCP). The project demonstrates the use of various GCP services to build a scalable and resilient system that can handle a high volume of events.

The main components of the architecture are:

- API Gateway: An API Gateway is a service that sits in front of your backend services and functions and acts as a reverse proxy. You can define the APIs using OpenAPI/Swagger specification.

- Cloud Functions: These are serverless functions that can be triggered by events, such as incoming http requests. They can be written in a variety of languages, including Node.js, Python, and Go.

- Workflows: In an event-driven serverless architecture, workflows can be used to coordinate the execution of multiple functions in a specific order. 

- Cloud Pub/Sub: This is a fully managed messaging service that allows for the sending and receiving of messages between independent applications. It can be used to trigger functions in response to incoming events.


![GCP OLTP with orchestration (2)](https://user-images.githubusercontent.com/987237/211893022-d225ff48-b3f2-48c1-ae66-137dd2087576.png)

<br><br>

# Deploying the services

## GCP Console setup
- Create project in GCP Console: https://console.cloud.google.com/

- Confirm billing is enabled for project


- Ensure project is selected in console and note project ID

## Local environment setup
- Download Google Cloud CLI
https://cloud.google.com/sdk/docs/install-sdk


- In shell, set local environment variables (fill in your specific details)
> export PROJECT_ID=myproject-12345\
> export REGION=us-west2

- Initialize project
> gcloud init

- Ensure the project is set to default:
> gcloud config set project $PROJECT_ID

- Run bash commands at project root to update config (make sure PROJECT_ID and REGION vars are set):
> grep -rl MY_GCP_PROJECT . | xargs sed -i -e 's/MY_GCP_PROJECT/'"$PROJECT_ID"'/g'

> grep -rl MY_GCP_REGION . | xargs sed -i -e 's/MY_GCP_REGION/'"$REGION"'/g'

- Enable GCP services
> gcloud services enable apigateway.googleapis.com \
gcloud services enable servicemanagement.googleapis.com \
gcloud services enable servicecontrol.googleapis.com

## Service Account setup

- Create Service Account
> gcloud iam service-accounts create service-account-01 \ \
    --description="Service account for API Gateway" \ \
    --display-name="service-account-01"

- List service accounts and note email:
> gcloud iam service-accounts list

- Set local environment service account (fill in your specific details)
> export SERVICE_ACCOUNT_EMAIL=service-account-01@myproject-12345.iam.gserviceaccount.com

## API Gateway setup

- Check API Gateway configs and enable if needed:
> gcloud api-gateway api-configs list

- Create new API and API Gateway configuration:
> gcloud api-gateway api-configs create api-gateway-v01 \ \
  --api=api-gateway --openapi-spec=api-gateway.yaml \ \
  --project=$PROJECT_ID \ \
  --backend-auth-service-account=$SERVICE_ACCOUNT_EMAIL

-  Listing the api configs should show the newly created config:
> gcloud api-gateway api-configs list 

- Get the managed service name:
> gcloud api-gateway apis list | awk '{print $3}'

- Enable API service (use your managed service name):
> gcloud services enable api-gateway-1234568k9easd.apigateway.gcp-test-01-123456.cloud.goog

- Create API Gateway:
> gcloud api-gateway gateways create my-api-gateway \ \
  --api=api-gateway --api-config=api-gateway-v01 \ \
  --location=$REGION \ \
  --project=$PROJECT_ID 

- Verify API Gateway has been created:
> gcloud api-gateway gateways list

- To update API Gateway after new config gets deployed:
> gcloud api-gateway gateways update my-api-gateway \ \
--api=api-gateway --api-config=api-gateway-v02 \ \
--location=$REGION

## Cloud Functions setup

- Deploy function for routing API calls to workflows (enable cloudfunctions and cloudbuild if prompted):
> gcloud functions deploy api_gateway --trigger-http \ \
  --runtime python39 --source cloud-function/api-gateway \ \
  --entry-point api_gateway \ \
  --region $REGION

- Deploy function for posting adjustments:
> gcloud functions deploy post_adjustment --trigger-http \ \
  --runtime python39 --source cloud-function/data \ \
  --entry-point post_adjustment \ \
  --region $REGION

## Workflows setup

- Deploy "Post Adjustment" workflow (enable `workflows.googleapis.com` if prompted)
> gcloud workflows deploy postAdjustmentWorkflow \ \
  --source workflows/post-adjustment-workflow.yaml \ \
  --location=$REGION


## Test it out

- Get the API Gateway url:
> gcloud api-gateway gateways describe my-api-gateway \ \
--location $REGION | grep defaultHostname

>https://my-api-gateway-9z0jgy8a.wl.gateway.dev/adjustments

> curl -X POST https://my-api-gateway-9z0jgy8a.wl.gateway.dev/adjustments

> {"message":"UNAUTHENTICATED:Method doesn't allow unregistered callers"}

## Security setup

- Create API key:
> gcloud alpha services api-keys create --display-name=api_key_test-01

- Copy the "keystring" value:
> "keyString":"AIzaSyAyKasdfasdfasdfsdf"

- Test the curl call again using the API key:
> curl -X POST https://my-api-gateway-123456.wl.gateway.dev/adjustments?key=AIzaSyAyKasdfasdfasdfsdf

See section on "Securing access by using an API key":
https://cloud.google.com/api-gateway/docs/secure-traffic-gcloud


<br><br>
## Notes

> gcloud basic commands:
>  - gcloud auth list
>  - gcloud config list
>  - gcloud info
>  - gcloud help
>    (i.e. gcloud help compute instances create)
