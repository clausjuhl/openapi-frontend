from typing import Dict

from starlette.templating import Jinja2Templates
from starlette.requests import Request

templates = Jinja2Templates(directory="templates")
# templates.env.filters['marked'] = marked_filter


def render(
    template: str, context: Dict, status_code: int = 200
) -> templates.TemplateResponse:

    headers = dict()
    # criteria = [request.app.debug, False]
    # if not any(criteria):
    headers[
        "Strict-Transport-Security"
    ] = "max-age=63072000; includeSubDomains"
    headers["X-Content-Type-Options"] = "nosniff"
    headers["X-Frame-Options"] = "DENY"
    headers["X-XSS-Protection"] = "1; mode=block"
    headers[
        "Content-Security-Policy"
    ] = "frame-ancestors 'none'; default-src 'none'; img-src 'self'; connect-src 'self'; script-src 'self'; style-src 'self'"
    return templates.TemplateResponse(
        template, context, headers=headers, status_code=status_code
    )
