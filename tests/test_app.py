import os
from types import SimpleNamespace

import pytest

# Prevent tests from requiring real AWS/OpenAI/LangSmith connections.
os.environ["ENABLE_CLOUDWATCH_LOGGING"] = "false"
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["LANGSMITH_TRACING"] = "false"

from fastapi.testclient import TestClient

import app.main as main_module
from app.main import app
from app.scenarios import apply_lab_scenario
from app.tools import get_vehicle_details


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ai-support-lab"
    }


def test_normal_chat(monkeypatch):
    def fake_create(**kwargs):
        return SimpleNamespace(
            output_text="DNS translates domain names into IP addresses."
        )

    monkeypatch.setattr(
        main_module.client.responses,
        "create",
        fake_create
    )

    response = client.post(
        "/chat",
        json={
            "customer_id": "CUST-100",
            "message": "What is DNS?"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["customer_id"] == "CUST-100"
    assert "DNS" in body["response"]


def test_vehicle_scenario_contains_tool_data():
    result = apply_lab_scenario(
        customer_id="INC004",
        message="Give me vehicle details."
    )

    assert "Demo Family SUV" in result
    assert '"seats": 5' in result
    assert '"status": "available"' in result


def test_bad_context_scenario_is_corrected():
    result = apply_lab_scenario(
        customer_id="INC005",
        message="What is the refund window?"
    )

    assert "30 days" in result
    assert "60 days" not in result


def test_tool_not_found():
    with pytest.raises(ValueError, match="Vehicle not found"):
        get_vehicle_details("INVALID-404")


def test_tool_failure_classification(monkeypatch):
    def fake_scenario(**kwargs):
        raise ValueError("Vehicle not found: INVALID-404")

    monkeypatch.setattr(
        main_module,
        "apply_lab_scenario",
        fake_scenario
    )

    response = client.post(
        "/chat",
        json={
            "customer_id": "TEST-TOOL-ERROR",
            "message": "Find invalid vehicle."
        }
    )

    assert response.status_code == 404

    body = response.json()

    assert body["detail"]["error_category"] == "TOOL_NOT_FOUND"
    assert body["detail"]["error"] == "Vehicle lookup failed"
