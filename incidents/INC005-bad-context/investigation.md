# INC005 - Investigation

## Symptom

The customer received an incorrect refund policy response.

## Investigation Steps

1. Reproduced the request using customer ID INC005.
2. Confirmed the API returned HTTP 200.
3. Checked AWS CloudWatch and confirmed the request completed successfully.
4. Opened the corresponding LangSmith trace.
5. Reviewed the model input.
6. Found that the application supplied the following context:

   "Refund requests are accepted within 60 days of purchase."

7. Compared this with the correct lab policy of 30 days.
8. Confirmed that the model followed the incorrect context it was given.

## Findings

The model was functioning as instructed.

The incorrect response originated from bad context supplied by the application.

## Root Cause

Incorrect policy context was injected into the model input.

## Component Responsible

Application context / prompt construction layer.

## Not Responsible

- OpenAI model availability
- AWS CloudWatch
- LangSmith
- Network connectivity
- API request validation
