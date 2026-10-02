from langsmith import traceable


VEHICLES = {
    "SUV-101": {
        "name": "Demo Family SUV",
        "seats": 5,
        "status": "available"
    }
}


@traceable(name="get_vehicle_details", run_type="tool")
def get_vehicle_details(vehicle_id: str):
    if vehicle_id not in VEHICLES:
        raise ValueError(f"Vehicle not found: {vehicle_id}")

    return VEHICLES[vehicle_id]
