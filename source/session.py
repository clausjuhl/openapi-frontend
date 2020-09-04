from typing import Dict

from starlette.requests import Request


def generate_session(session: Request.session) -> Dict:
    return {"traversion": True, "current_id": 1412}

