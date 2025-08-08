import os
import sys
import types

import pytest
from unittest.mock import MagicMock, patch

# Stub external dependencies to avoid heavy imports
langchain_module = types.ModuleType('langchain')
text_splitter_module = types.ModuleType('langchain.text_splitter')
class RecursiveCharacterTextSplitter:
    def __init__(self, *args, **kwargs):
        pass
    def split_text(self, text):
        return [text]
text_splitter_module.RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter
langchain_module.text_splitter = text_splitter_module
sys.modules['langchain'] = langchain_module
sys.modules['langchain.text_splitter'] = text_splitter_module

llm_client_module = types.ModuleType('llm_client')
embedding_module = types.ModuleType('llm_client.embedding')
def generate_embeddings(chunks, model='text-embedding-3-small'):
    return []
embedding_module.generate_embeddings = generate_embeddings
llm_client_module.embedding = embedding_module
sys.modules['llm_client'] = llm_client_module
sys.modules['llm_client.embedding'] = embedding_module

vector_db_module = types.ModuleType('vector_db_manager')
chroma_module = types.ModuleType('vector_db_manager.chroma')
def get_or_create_collection(name='iso_documents'):
    return None
def store_document_chunks(collection, chunks, embeddings, doc_id):
    pass
chroma_module.get_or_create_collection = get_or_create_collection
chroma_module.store_document_chunks = store_document_chunks
vector_db_module.chroma = chroma_module
sys.modules['vector_db_manager'] = vector_db_module
sys.modules['vector_db_manager.chroma'] = chroma_module

from services.document_service import process_and_store_document

# Clean up stubbed modules to avoid affecting other tests
for mod in [
    'langchain',
    'langchain.text_splitter',
    'llm_client',
    'llm_client.embedding',
    'vector_db_manager',
    'vector_db_manager.chroma',
]:
    sys.modules.pop(mod, None)


@pytest.fixture
def sample_input():
    return b"Hello world", "text/plain", "sample.txt"


def test_process_and_store_document_success(sample_input):
    file_content, file_type, name = sample_input
    mock_embedding = [[0.1, 0.2, 0.3]]

    with patch("services.document_service.generate_embeddings", return_value=mock_embedding) as embed_mock, \
         patch("services.document_service.get_or_create_collection", return_value=MagicMock()) as get_coll_mock, \
         patch("services.document_service.store_document_chunks") as store_mock:
        doc_id, num_chunks = process_and_store_document(file_content, file_type, name)

        assert doc_id.startswith("doc_")
        assert num_chunks == 1

        embed_mock.assert_called_once()
        get_coll_mock.assert_called_once()
        store_mock.assert_called_once()


def test_process_and_store_document_embedding_failure(sample_input):
    file_content, file_type, name = sample_input

    with patch("services.document_service.generate_embeddings", side_effect=Exception("fail")) as embed_mock, \
         patch("services.document_service.get_or_create_collection") as get_coll_mock, \
         patch("services.document_service.store_document_chunks") as store_mock:
        with pytest.raises(Exception, match="fail"):
            process_and_store_document(file_content, file_type, name)

        embed_mock.assert_called_once()
        get_coll_mock.assert_not_called()
        store_mock.assert_not_called()
