# INC003 - Investigation

## Symptom

The AI assistant returned a correct response, but the request took significantly longer than normal.

## Investigation Steps

1. Reproduced the issue using customer ID INC003.
2. Confirmed the API returned HTTP 200.
3. Checked AWS CloudWatch application logs.
4. CloudWatch showed a total request duration of approximately 9811 ms.
5. Opened the corresponding LangSmith trace.
6. LangSmith showed the model call took approximately 4.73 seconds.
7. Compared total request duration with model duration.
8. Identified approximately 5 seconds of additional latency outside the model call.
9. Reviewed application logic and found a deliberate 5-second delay before the OpenAI request.

## Findings

The LLM was not responsible for the full response delay.

The model call accounted for approximately 4.73 seconds.

The remaining approximately 5 seconds occurred inside the application before the model request was sent.

## Root Cause

Application-layer processing introduced a 5-second delay before the LLM call.

## Component Responsible

FastAPI application processing layer.

## Not Responsible

- OpenAI model availability
- LangSmith
- AWS CloudWatch
- API request validation
