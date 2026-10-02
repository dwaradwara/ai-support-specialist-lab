# INC004 - Tool Failure

## Customer Report

Customer requested vehicle details but the AI service returned an error.

## Customer ID

INC004

## Request

"Give me the details for vehicle INVALID-404."

## Actual Result

HTTP 502 Bad Gateway.

Customer-facing error:

"LLM request failed"

## Impact

The request failed because the backend vehicle lookup tool could not find the requested vehicle.

## Severity

Low - controlled lab incident.

## Status

Resolved

