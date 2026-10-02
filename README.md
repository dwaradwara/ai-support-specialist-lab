@'
# AI SaaS Support Engineering Lab

A hands-on support engineering lab built to demonstrate troubleshooting, observability, incident response, AI/LLM support, AWS logging, LangSmith tracing, customer communication, and user lifecycle operations.

## Purpose

This project simulates the responsibilities of an AI SaaS Support Specialist supporting customer-facing AI applications.

The focus is not model development. The focus is identifying whether a customer issue originates from:

- application logic
- LLM/API behavior
- prompt or context quality
- backend tools
- latency
- configuration
- upstream dependencies

## Architecture

```text
Customer
   |
   v
FastAPI /chat
   |
   +--> Request ID
   |       |
   |       +--> AWS CloudWatch structured logs
   |
   +--> Application processing
   |
   +--> Backend tools
   |       |
   |       +--> get_vehicle_details()
   |
   +--> OpenAI model
           |
           +--> LangSmith tracing
                   |
                   +--> Input
                   +--> Output
                   +--> Latency
                   +--> Errors
                   +--> Tool traces