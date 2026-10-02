import json

from app.tools import get_vehicle_details


def apply_lab_scenario(
    customer_id: str,
    message: str
) -> str:
    """
    Apply controlled lab-only scenario context.

    Production application logic should not depend on incident IDs.
    These branches exist only to reproduce support scenarios.
    """

    if customer_id == "INC005":
        return (
            "Company policy context: "
            "Refund requests are accepted within 30 days of purchase."
            + "\n\nCustomer question: "
            + message
        )

    if customer_id == "INC004":
        vehicle_details = get_vehicle_details("SUV-101")

        return (
            message
            + "\n\nVehicle lookup result:\n"
            + json.dumps(vehicle_details)
        )

    return message
