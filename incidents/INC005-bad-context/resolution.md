# INC005 - Resolution

## Root Cause

The application supplied incorrect policy context to the model.

The model received a 60-day refund policy and correctly followed that context, even though the real lab policy was 30 days.

## Resolution

Updated the application context from:

"Refund requests are accepted within 60 days of purchase."

to:

"Refund requests are accepted within 30 days of purchase."

## Validation

1. Repeated the original request:
   "What is the refund window?"

2. API returned HTTP 200.

3. Customer-facing response correctly stated 30 days.

4. LangSmith showed the corrected 30-day context in the model input.

5. The model output matched the expected policy.

## Result

Incident resolved.

## Prevention

- Validate business context before sending it to the model.
- Review LangSmith inputs when AI responses contain incorrect policy information.
- Do not automatically classify incorrect answers as hallucinations.
- Treat retrieved or injected context as a potential source of incorrect AI behavior.
