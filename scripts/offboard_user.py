import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "users.json"


def load_users():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_users(users):
    DATA_FILE.write_text(
        json.dumps(users, indent=2),
        encoding="utf-8"
    )


parser = argparse.ArgumentParser(description="Offboard a support user")
parser.add_argument("--email", required=True)

args = parser.parse_args()

users = load_users()

for user in users:
    if user["email"].lower() == args.email.lower():
        user["status"] = "disabled"
        user["role"] = "revoked"
        user["disabled_at"] = datetime.now(timezone.utc).isoformat()

        save_users(users)

        print(json.dumps({
            "event": "user_offboarded",
            "email": args.email,
            "role": "revoked",
            "status": "disabled"
        }, indent=2))

        break
else:
    raise SystemExit(f"User not found: {args.email}")
