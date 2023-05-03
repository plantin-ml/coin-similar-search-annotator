import uuid
from typing import List


def generate_task_id() -> str:
    """Return unique string for task id."""

    return uuid.uuid4().hex


def form_error_message(errors: List[dict]) -> List[str]:
    """
    Make valid pydantic `ValidationError` messages list.
    """

    messages = []
    for error in errors:
        field, message = error["loc"][-1], error["msg"]
        messages.append(f"`{field}` {message}")
    return messages
