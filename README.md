# AI SaaS Support Engineering Lab

A hands-on AI SaaS support engineering lab focused on troubleshooting, observability, incident response, customer communication, and technical escalation.

The project simulates the work of a Support Specialist responsible for diagnosing customer-facing AI product issues using **Python, FastAPI, OpenAI, LangSmith, and AWS CloudWatch**.

> All incidents in this repository are intentionally simulated in a controlled lab environment. They do not represent production customer incidents.

---

## Project Goals

The objective of this lab is not to build a complex AI product.

The objective is to demonstrate how a technical support specialist can identify whether an issue originates from:

- application logic
- LLM/API communication
- prompt or context quality
- backend tools
- latency
- configuration
- upstream dependencies

The lab also demonstrates customer communication, engineering escalation, SOP documentation, and basic user onboarding/offboarding workflows.

---

## Architecture

```text
Customer
   |
   v
FastAPI /chat
   |
   +----> Generate Request ID
   |          |
   |          +----> AWS CloudWatch
   |                 Structured Application Logs
   |
   +----> Application Processing
   |
   +----> Backend Tools
   |          |
   |          +----> get_vehicle_details()
   |
   +----> OpenAI API
              |
              +----> LangSmith
                     LLM / Tool Tracing
                     |
                     +---- Input
                     +---- Output
                     +---- Latency
                     +---- Errors
                     +---- Tool Execution
```

The request ID allows customer-facing API activity to be correlated with application logs during incident investigation.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and support automation |
| FastAPI | Customer-facing API |
| OpenAI API | AI response generation |
| LangSmith | LLM and tool tracing |
| AWS CloudWatch | Centralized application logging |
| Boto3 | AWS SDK |
| Watchtower | Python logging to CloudWatch |
| Pydantic | Request validation |
| Uvicorn | ASGI application server |
| Git / GitHub | Version control and portfolio documentation |

---

## Observability

### AWS CloudWatch

Application events are written as structured JSON logs.

Example:

```json
{
  "event": "chat_request_completed",
  "request_id": "example-request-id",
  "customer_id": "CUST-101",
  "duration_ms": 3712.82,
  "status": "success"
}
```

Logged fields include:

- request ID
- customer ID
- event type
- duration
- status
- error category
- responsible component

This allows support engineers to correlate a customer's request with backend application behavior.

### LangSmith

LangSmith is used to inspect the AI execution layer, including:

- model input
- system instructions
- model output
- model latency
- token usage
- model/API errors
- backend tool execution
- tool inputs and outputs

CloudWatch and LangSmith serve different purposes:

```text
CloudWatch
Application / operational behavior

LangSmith
LLM / prompt / tool behavior
```

Using both makes it possible to isolate which layer is actually responsible for a customer issue.

---

## Error Classification

The application separates common failure categories instead of treating every AI issue as the same problem.

| Error Category | Meaning |
|---|---|
| `LLM_TIMEOUT` | AI provider request exceeded the configured timeout |
| `TOOL_NOT_FOUND` | Backend tool or lookup failed |
| `MODEL_API_ERROR` | AI provider/API request failed |
| `APPLICATION_ERROR` | Unexpected application-layer failure |

This provides clearer logging and faster incident triage.

---

# Incident Scenarios

## INC001 — Incorrect Customer Response

### Symptom

The customer received incorrect information:

```text
Yes. HTTP traffic is encrypted by default.
```

The API still returned HTTP `200`.

### Investigation

CloudWatch showed that the application request completed successfully.

LangSmith showed that the model itself produced the correct answer:

```text
Plain HTTP is not encrypted by default.
```

The customer-facing response differed from the actual model output.

### Root Cause

Application response-processing logic modified the correct LLM response before returning it to the customer.

### Key Support Lesson

An incorrect AI response does not automatically mean the LLM hallucinated.

Support must compare:

```text
Customer response
vs
Model output
vs
Application processing
```

### Evidence

[Swagger — incorrect customer response](incidents/INC001-wrong-ai-response/evidence/01-swagger-incorrect-response.png)

[LangSmith — correct model output](incidents/INC001-wrong-ai-response/evidence/02-langsmith-correct-model-output.png)

---

## INC002 — LLM API Timeout

### Symptom

The customer request returned:

```text
HTTP 502 Bad Gateway
```

### Investigation

CloudWatch recorded:

```text
chat_request_failed
APITimeoutError
```

LangSmith showed:

```text
APITimeoutError: Request timed out
No model output
```

### Root Cause

The OpenAI client was configured with an unrealistically aggressive timeout.

### Resolution

The bad timeout configuration was removed and the same request completed successfully.

### Key Support Lesson

A failed AI request may be caused by application/client configuration rather than the model itself.

### Evidence

[Swagger — timeout response](incidents/INC002-llm-timeout/evidence/01-swagger-502-timeout.png)

[LangSmith — API timeout](incidents/INC002-llm-timeout/evidence/02-langsmith-api-timeout-error.png)

[CloudWatch — timeout log](incidents/INC002-llm-timeout/evidence/03-cloudwatch-timeout-log.png)

---

## INC003 — High Latency

### Symptom

The request returned successfully, but customer response time was unusually high.

### Measurements

CloudWatch total request duration:

```text
9811.26 ms
```

LangSmith model duration:

```text
~4.73 seconds
```

Difference:

```text
~5 seconds
```

The comparison showed that a significant portion of the latency occurred outside the LLM call.

### Root Cause

The application processing layer introduced an unnecessary five-second delay before sending the model request.

### Resolution

The application delay was removed.

Post-fix CloudWatch duration:

```text
3712.82 ms
```

### Key Support Lesson

Do not automatically blame model latency.

Compare:

```text
Total application duration
-
Model duration
=
Non-model application latency
```

### Evidence

[CloudWatch — 9811 ms request](incidents/INC003-high-latency/evidence/01-cloudwatch-high-latency-9811ms.png)

[LangSmith — model latency](incidents/INC003-high-latency/evidence/02-langsmith-model-latency-4730ms.png)

[Swagger — successful post-fix request](incidents/INC003-high-latency/evidence/03-swagger-post-fix-success.png)

[LangSmith — post-fix trace](incidents/INC003-high-latency/evidence/04-langsmith-post-fix-3640ms.png)

---

## INC004 — Backend Tool Failure

### Symptom

A customer requested details for:

```text
INVALID-404
```

The API returned HTTP `502`.

### Investigation

LangSmith showed the backend tool failure:

```text
Tool: get_vehicle_details
Input: INVALID-404

ValueError:
Vehicle not found: INVALID-404
```

No valid tool output was produced.

The application originally classified this incorrectly as an LLM failure.

### Root Cause

The vehicle lookup tool received an invalid vehicle identifier and raised an exception.

### Resolution

The workflow was updated to:

- distinguish tool failures from LLM failures
- use explicit error categories
- pass successful tool output into the model context

A successful lookup for `SUV-101` returned:

```text
Demo Family SUV
Seats: 5
Status: available
```

### Engineering Escalation

This incident also contains a structured engineering escalation documenting:

- customer impact
- reproduction steps
- observed behavior
- root cause
- proposed engineering change
- validation criteria

[View engineering escalation](incidents/INC004-tool-failure/engineering-escalation.md)

### Evidence

[Swagger — tool failure](incidents/INC004-tool-failure/evidence/01-swagger-tool-failure-502.png)

[LangSmith — vehicle lookup failure](incidents/INC004-tool-failure/evidence/02-langsmith-vehicle-not-found.png)

[Swagger — successful tool result](incidents/INC004-tool-failure/evidence/03-swagger-valid-tool-result.png)

---

## INC005 — Incorrect AI Context

### Symptom

The customer asked:

```text
What is the refund window?
```

The AI incorrectly answered:

```text
60 days
```

The correct lab policy was:

```text
30 days
```

### Investigation

The API returned HTTP `200`, indicating no infrastructure failure.

LangSmith revealed that the application itself supplied this context:

```text
Company policy context:
Refund requests are accepted within 60 days of purchase.
```

The model then correctly followed the incorrect context it had been given.

### Root Cause

Incorrect business context was supplied to the model by the application.

### Resolution

The application context was corrected to:

```text
Refund requests are accepted within 30 days of purchase.
```

The same request then returned the correct 30-day policy.

### Key Support Lesson

Incorrect AI output can originate from bad context rather than hallucination or model failure.

### Evidence

[Swagger — incorrect 60-day response](incidents/INC005-bad-context/evidence/01-swagger-wrong-60-day-context-response.png)

[LangSmith — incorrect context supplied to model](incidents/INC005-bad-context/evidence/02-langsmith-bad-context-60-days.png)

[Swagger — corrected 30-day response](incidents/INC005-bad-context/evidence/03-post-fix-swagger-30-days.png)

---

# Support Investigation Workflow

The standard troubleshooting workflow used throughout the lab is:

```text
Customer reports issue
        |
        v
Collect customer ID / request ID / timestamp
        |
        v
Reproduce the issue
        |
        v
Check HTTP response
        |
        v
Search AWS CloudWatch
        |
        v
Inspect LangSmith trace
        |
        v
Identify failure layer
        |
        +---- Application
        |
        +---- LLM / API
        |
        +---- Prompt / Context
        |
        +---- Backend Tool
        |
        +---- Latency
        |
        +---- Upstream Dependency
        |
        v
Resolve or Escalate
        |
        v
Validate fix
        |
        v
Update customer
        |
        v
Document incident
```

The full SOP is available here:

[AI Support Incident Triage SOP](docs/support-sop.md)

---

# Incident Documentation

Each incident contains support-focused documentation.

Typical structure:

```text
ticket.md
investigation.md
resolution.md
customer-response.md
evidence/
```

INC004 additionally includes:

```text
engineering-escalation.md
```

This demonstrates both customer-facing communication and technical escalation to engineering.

---

# User Onboarding and Offboarding

The repository also includes small Python scripts demonstrating user lifecycle support tasks.

```text
scripts/
├── onboard_user.py
└── offboard_user.py
```

### Onboarding

```text
Create user
   |
Assign role
   |
Activate account
```

Example:

```powershell
python scripts\onboard_user.py `
  --name "Demo User" `
  --email "demo@example.com" `
  --role "support_agent"
```

### Offboarding

```text
Locate user
   |
Revoke role
   |
Disable account
```

Example:

```powershell
python scripts\offboard_user.py `
  --email "demo@example.com"
```

The resulting demo account is stored in:

```text
data/users.json
```

---

# Running the Lab

## 1. Clone the repository

```bash
git clone https://github.com/dwaradwara/ai-support-specialist-lab.git
cd ai-support-specialist-lab
```

## 2. Create a virtual environment

Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## 4. Configure environment variables

Create:

```text
.env
```

Example:

```text
OPENAI_API_KEY=your_openai_api_key

LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=ai-support-specialist-lab
```

Do not commit `.env`.

## 5. AWS authentication

The application sends logs to:

```text
/ai-support-specialist-lab/application
```

AWS region:

```text
eu-central-1
```

AWS credentials must be configured separately on the machine running the application.

## 6. Start the API

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

---

# Repository Structure

```text
ai-support-specialist-lab/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── logging_config.py
│   └── tools.py
│
├── data/
│   └── users.json
│
├── docs/
│   └── support-sop.md
│
├── incidents/
│   ├── INC001-wrong-ai-response/
│   ├── INC002-llm-timeout/
│   ├── INC003-high-latency/
│   ├── INC004-tool-failure/
│   └── INC005-bad-context/
│
├── scripts/
│   ├── onboard_user.py
│   └── offboard_user.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Security

Sensitive values are stored in `.env`, which is excluded through `.gitignore`.

The repository should never contain:

- OpenAI API keys
- LangSmith API keys
- AWS secret/access keys
- passwords
- production customer data

Example `.gitignore`:

```text
.venv/
.env
__pycache__/
*.pyc
```

---

# Skills Demonstrated

This lab demonstrates practical experience with:

- AI SaaS technical support
- customer issue triage
- Python troubleshooting
- FastAPI
- OpenAI API integration
- AWS CloudWatch
- LangSmith observability
- structured logging
- request correlation
- LLM troubleshooting
- prompt/context investigation
- backend tool troubleshooting
- latency analysis
- root-cause analysis
- incident response
- customer-facing communication
- engineering escalation
- SOP creation
- basic user onboarding/offboarding

---

## Portfolio Context

This repository is a controlled support-engineering lab designed to demonstrate the investigation workflow used when supporting AI-enabled SaaS products.

The emphasis is on **diagnosing the correct failure layer using evidence rather than assuming that every AI-related issue is caused by the model**.