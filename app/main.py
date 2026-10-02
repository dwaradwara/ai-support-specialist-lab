import json
import time
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI, APITimeoutError, APIError
from langsmith.wrappers import wrap_openai

from app.logging_config import configure_logger
from app.scenarios import apply_lab_scenario


load_dotenv()

logger = configure_logger()

app = FastAPI(
    title="AI Support Specialist Lab",
    version="1.0.0"
)

client = wrap_openai(OpenAI())


class ChatRequest(BaseModel):
    customer_id: str
    message: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-support-lab"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(json.dumps({
        "event": "chat_request_received",
        "request_id": request_id,
        "customer_id": request.customer_id
    }))

    try:
        system_instruction = (
            "You are a helpful technical assistant. "
            "Answer accurately and concisely."
        )

        model_input = apply_lab_scenario(
            customer_id=request.customer_id,
            message=request.message
        )

        response = client.responses.create(
            model="gpt-6-luna",
            instructions=system_instruction,
            input=model_input
        )

        duration_ms = round(
            (time.time() - start_time) * 1000,
            2
        )

        logger.info(json.dumps({
            "event": "chat_request_completed",
            "request_id": request_id,
            "customer_id": request.customer_id,
            "duration_ms": duration_ms,
            "status": "success"
        }))

        return {
            "request_id": request_id,
            "customer_id": request.customer_id,
            "message": request.message,
            "response": response.output_text
        }

    except APITimeoutError:
        duration_ms = round(
            (time.time() - start_time) * 1000,
            2
        )

        logger.error(json.dumps({
            "event": "chat_request_failed",
            "request_id": request_id,
            "customer_id": request.customer_id,
            "duration_ms": duration_ms,
            "error_category": "LLM_TIMEOUT",
            "component": "openai",
            "status": "error"
        }))

        raise HTTPException(
            status_code=504,
            detail={
                "request_id": request_id,
                "error_category": "LLM_TIMEOUT",
                "error": "AI service timed out"
            }
        )

    except ValueError:
        duration_ms = round(
            (time.time() - start_time) * 1000,
            2
        )

        logger.error(json.dumps({
            "event": "chat_request_failed",
            "request_id": request_id,
            "customer_id": request.customer_id,
            "duration_ms": duration_ms,
            "error_category": "TOOL_NOT_FOUND",
            "component": "vehicle_lookup",
            "status": "error"
        }))

        raise HTTPException(
            status_code=404,
            detail={
                "request_id": request_id,
                "error_category": "TOOL_NOT_FOUND",
                "error": "Vehicle lookup failed"
            }
        )

    except APIError:
        duration_ms = round(
            (time.time() - start_time) * 1000,
            2
        )

        logger.error(json.dumps({
            "event": "chat_request_failed",
            "request_id": request_id,
            "customer_id": request.customer_id,
            "duration_ms": duration_ms,
            "error_category": "MODEL_API_ERROR",
            "component": "openai",
            "status": "error"
        }))

        raise HTTPException(
            status_code=502,
            detail={
                "request_id": request_id,
                "error_category": "MODEL_API_ERROR",
                "error": "AI provider request failed"
            }
        )

    except Exception as error:
        duration_ms = round(
            (time.time() - start_time) * 1000,
            2
        )

        logger.error(json.dumps({
            "event": "chat_request_failed",
            "request_id": request_id,
            "customer_id": request.customer_id,
            "duration_ms": duration_ms,
            "error_category": "APPLICATION_ERROR",
            "component": "application",
            "error_type": type(error).__name__,
            "status": "error"
        }))

        raise HTTPException(
            status_code=500,
            detail={
                "request_id": request_id,
                "error_category": "APPLICATION_ERROR",
                "error": "Internal application error"
            }
        )




