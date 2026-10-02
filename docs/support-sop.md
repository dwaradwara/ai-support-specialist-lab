# AI Support Incident Triage SOP

## Purpose

This SOP defines the standard process for investigating customer-reported issues in the AI Support Specialist Lab.

## 1. Collect Customer Information

For every incident collect:

- Customer ID
- Request ID
- Approximate timestamp
- Customer-reported symptom
- Expected behavior
- Actual behavior
- HTTP status if available

## 2. Reproduce the Issue

Attempt to reproduce the customer's request using the same input and conditions.

Record:

- request ID
- response
- HTTP status
- response time

## 3. Check Application Logs

Search AWS CloudWatch using the request ID.

Review:

- chat_request_received
- chat_request_completed
- chat_request_failed
- duration_ms
- error_type
- customer_id

Determine whether the application completed successfully or raised an exception.

## 4. Inspect LangSmith

Locate the corresponding AI or tool trace.

Check:

- model input
- system instructions
- model output
- latency
- token usage
- trace status
- tool calls
- tool inputs and outputs
- errors

## 5. Identify the Failure Layer

Classify the issue as one of the following:

- Application logic
- LLM/API timeout
- Model/prompt behavior
- Backend tool/API failure
- Input validation
- Latency/performance
- Upstream dependency
- Unknown / requires escalation

## 6. Determine Root Cause

Compare evidence from:

Customer symptom
→ API response
→ CloudWatch logs
→ LangSmith trace
→ application/tool behavior

Do not assume an incorrect AI response is automatically an LLM hallucination.

## 7. Resolve or Escalate

Resolve directly when the problem is within support scope.

Escalate to engineering when:

- code changes are required
- issue cannot be reproduced reliably
- repeated failures affect multiple customers
- tool/backend dependency requires engineering intervention
- data indicates a product defect

## 8. Validate the Resolution

Repeat the original customer request.

Confirm:

- expected response is returned
- HTTP status is correct
- CloudWatch shows successful completion
- LangSmith trace completes successfully
- tool output is correct when applicable

## 9. Customer Communication

Provide a concise update containing:

- acknowledgment of the issue
- what was found
- whether the problem has been resolved
- any action required from the customer

Avoid exposing internal stack traces, credentials, or sensitive implementation details.

## 10. Documentation

Update the incident documentation with:

- customer ticket
- investigation
- root cause
- resolution
- supporting evidence
- customer response
- engineering escalation when required
