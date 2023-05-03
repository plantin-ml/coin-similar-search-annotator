from collections.abc import Generator
from hashlib import sha256
import uuid


def generate_id() -> str:
    """Return unique string for task id."""

    return uuid.uuid4().hex

def chunks(lst: list, size: int) -> Generator:
    """Yield successive n-sized chunks from list."""
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def get_text_hash(text: str) -> str:
    """Get SHA256 hash from string"""

    return sha256(text.encode()).hexdigest()
