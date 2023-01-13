# GCP Architecture example

Demo project for an event-driven serverless architecture in Google Cloud Platform

This project is an example of an event-driven serverless architecture on Google Cloud Platform (GCP). The project demonstrates the use of various GCP services to build a scalable and resilient system that can handle a high volume of events.

The main components of the architecture are:

- API Gateway: An API Gateway is a service that sits in front of your backend services and functions and acts as a reverse proxy. You can define the APIs using OpenAPI/Swagger specification.

- Cloud Functions: These are serverless functions that can be triggered by events, such as incoming http requests. They can be written in a variety of languages, including Node.js, Python, and Go.

- Workflows: In an event-driven serverless architecture, workflows can be used to coordinate the execution of multiple functions in a specific order. 

- Cloud Pub/Sub: This is a fully managed messaging service that allows for the sending and receiving of messages between independent applications. It can be used to trigger functions in response to incoming events.

To deploy and run the example, you will need to have a GCP account and have the GCP CLI installed on your machine. 

![GCP OLTP with orchestration (2)](https://user-images.githubusercontent.com/987237/211893022-d225ff48-b3f2-48c1-ae66-137dd2087576.png)


# Project Setup

- Create project in GCP Console

- Confirm billing is enabled for project


- Ensure project is selected in console and note project ID

- Download Google Cloud CLI
https://cloud.google.com/sdk/docs/install-sdk


- Set local environment (fill in your specific details)
> export PROJECT_ID=myproject-12345\
> export REGION=us-west2


- Initialize project

> gcloud init

- Ensure the project is set to default:

> gcloud config set project $PROJECT_ID

- Replace all instances of MY_GCP_PROJECT with your project info

> grep -rl MY_GCP_PROJECT . | xargs sed -i -e 's/MY_GCP_PROJECT/'"$PROJECT_ID"'/g'

> grep -rl MY_GCP_REGION . | xargs sed -i -e 's/MY_GCP_REGION/'"$REGION"'/g'



- Create Service Account
> gcloud iam service-accounts create service-account-01 \ \
    --description="Service account for API Gateway" \ \
    --display-name="service-account-01"

- List service accounts and note email:
> gcloud iam service-accounts list

- Set local environment service account (fill in your specific details)
> export SERVICE_ACCOUNT_EMAIL=service-account-01@myproject-12345.iam.gserviceaccount.com

- Check API Gateway and enable if needed:
> gcloud api-gateway api-configs list

- Create new API Gateway configuration
> gcloud api-gateway api-configs create api-gateway-v01 \ \
  --api=api-gateway --openapi-spec=api-gateway.yaml \ \
  --project=$PROJECT_ID \ \
  --backend-auth-service-account=$SERVICE_ACCOUNT_EMAIL

-  Listing the api configs should show the newly created config:
> gcloud api-gateway api-configs list 



## Notes

> gcloud basic commands:
>  - gcloud auth list
>  - gcloud config list
>  - gcloud info
>  - gcloud help
>    (i.e. gcloud help compute instances create)
