import sys
import logging
from unittest.mock import patch, MagicMock


def test_generate_embeddings_logs_and_returns_empty_list_on_error(caplog):
    with patch("utils.helpers.load_env_variables", return_value={"OPENAI_API_KEY": "test"}), \
         patch("openai.OpenAI", return_value=MagicMock()):
        if "llm_client.embedding" in sys.modules:
            del sys.modules["llm_client.embedding"]
        import llm_client.embedding as emb

    with patch.object(emb.client.embeddings, "create", side_effect=Exception("boom")), \
         caplog.at_level(logging.ERROR):
        result = emb.generate_embeddings(["hello"])
        assert result == []
        assert "An error occurred while generating embeddings" in caplog.text

    sys.modules.pop("llm_client.embedding", None)
