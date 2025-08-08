import uuid

from vector_db_manager.chroma import (
    get_or_create_collection,
    store_document_chunks,
    search_similar_chunks,
    build_document_filter,
)


def test_search_similar_chunks_filters_by_document_id():
    collection = get_or_create_collection(name=f"test_{uuid.uuid4()}")

    embedding = [0.1, 0.2, 0.3]
    store_document_chunks(collection, ["doc1 chunk"], [embedding], "doc1")
    store_document_chunks(collection, ["doc2 chunk"], [embedding], "doc2")

    results = search_similar_chunks(
        collection,
        embedding,
        top_k=5,
        where=build_document_filter("doc1"),
    )

    assert results == ["doc1 chunk"]
