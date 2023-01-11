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
