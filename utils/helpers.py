"""Utility helpers used across the project."""

import os

# ``python-dotenv`` is an optional dependency.  The test environment does not
# guarantee its presence, so we attempt to import it gracefully.  When the
# package is unavailable, ``load_dotenv`` becomes a no-op function, allowing the
# rest of the helpers to rely solely on environment variables already set.
try:  # pragma: no cover - simple import guard
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - environment without python-dotenv
    def load_dotenv(*_args, **_kwargs):  # type: ignore
        return None

def validate_file_type(file_name):
    """
    Validates the file type based on its extension.
    Allowed extensions: .pdf, .docx, .txt
    """
    allowed_extensions = ['.pdf', '.docx', '.txt']
    ext = os.path.splitext(file_name)[1]
    return ext.lower() in allowed_extensions

def load_env_variables():
    """Load required environment variables using python-dotenv.

    Returns a dictionary containing the OpenAI API key.

    Raises:
        ValueError: If ``OPENAI_API_KEY`` is not set.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    return {"OPENAI_API_KEY": api_key}
