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


parser = argparse.ArgumentParser(description="Onboard a support user")
parser.add_argument("--name", required=True)
parser.add_argument("--email", required=True)
parser.add_argument("--role", required=True)

args = parser.parse_args()

users = load_users()

if any(user["email"].lower() == args.email.lower() for user in users):
    raise SystemExit(f"User already exists: {args.email}")

user = {
    "name": args.name,
    "email": args.email,
    "role": args.role,
    "status": "active",
    "created_at": datetime.now(timezone.utc).isoformat()
}

users.append(user)
save_users(users)

print(json.dumps({
    "event": "user_onboarded",
    "email": args.email,
    "role": args.role,
    "status": "active"
}, indent=2))
