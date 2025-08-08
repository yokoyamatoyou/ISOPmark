import sys
from unittest.mock import patch


def test_embedding_uses_helper():
    with patch("utils.helpers.load_env_variables", return_value={"OPENAI_API_KEY": "test"}) as mock_env, \
         patch("openai.OpenAI"):
        if "llm_client.embedding" in sys.modules:
            del sys.modules["llm_client.embedding"]
        import llm_client.embedding  # noqa: F401
        mock_env.assert_called_once()


def test_completion_uses_helper():
    with patch("utils.helpers.load_env_variables", return_value={"OPENAI_API_KEY": "test"}) as mock_env, \
         patch("openai.OpenAI"):
        if "llm_client.completion" in sys.modules:
            del sys.modules["llm_client.completion"]
        import llm_client.completion  # noqa: F401
        mock_env.assert_called_once()
