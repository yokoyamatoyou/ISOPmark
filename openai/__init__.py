"""Minimal stub of the :mod:`openai` package used in tests.

Only the ``OpenAI`` class is provided so that unit tests can patch it without
requiring the real external dependency.
"""


class OpenAI:  # pragma: no cover - simple stub
    def __init__(self, *args, **kwargs):
        pass

