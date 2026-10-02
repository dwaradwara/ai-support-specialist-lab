# Engineering Escalation - INC004

## Issue

Vehicle lookup requests can fail when an invalid vehicle ID is supplied.

## Customer Impact

The customer receives an HTTP 502 response instead of a clear vehicle-not-found response.

## Reproduction

1. Send POST /chat.
2. Use customer_id INC004.
3. Request vehicle INVALID-404.
4. Observe backend tool failure.

## Observed Behavior

Tool:
get_vehicle_details

Input:
INVALID-404

Result:
ValueError: Vehicle not found: INVALID-404

LangSmith:
Tool execution failed with no output.

Application:
Generic error handler classified the failure as an LLM request failure.

## Expected Behavior

The application should:

1. detect an invalid vehicle ID
2. classify the error as a vehicle lookup failure
3. return an appropriate customer-facing response
4. avoid incorrectly identifying the issue as an LLM failure

## Root Cause

The vehicle lookup tool raised ValueError for an unknown vehicle ID and the application did not initially distinguish tool failures from LLM failures.

## Recommended Engineering Change

Add explicit tool exception handling and error classification for vehicle lookup failures.

Suggested classification:

TOOL_NOT_FOUND

Component:

vehicle_lookup

## Validation Criteria

- Valid vehicle ID returns vehicle data.
- Invalid vehicle ID produces a controlled lookup error.
- Error is logged with the correct component and category.
- Customer does not receive a misleading LLM failure message.
