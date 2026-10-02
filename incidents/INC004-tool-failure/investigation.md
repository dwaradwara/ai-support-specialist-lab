# INC004 - Investigation

## Symptom

The /chat endpoint returned HTTP 502 while processing a vehicle-details request.

## Investigation Steps

1. Reproduced the issue using customer ID INC004.
2. Captured the request ID from the API response.
3. Checked the corresponding LangSmith trace.
4. LangSmith showed the get_vehicle_details tool failed.
5. Tool input was vehicle_id=INVALID-404.
6. LangSmith recorded ValueError: Vehicle not found: INVALID-404.
7. The tool produced no output.
8. The exception propagated to the application error handler.
9. The API returned HTTP 502 with the generic message "LLM request failed".

## Findings

The OpenAI model was not the source of the failure.

The backend vehicle lookup tool received an invalid vehicle ID and raised ValueError.

The application also misclassified the tool failure as an LLM failure.

## Root Cause

Invalid vehicle ID caused get_vehicle_details() to fail with ValueError.

## Component Responsible

Backend tool / application tool-handling layer.

## Not Responsible

- OpenAI model
- LangSmith
- AWS CloudWatch
- FastAPI request validation
