"""Light‑weight in-memory vector store used for tests.

This module replaces the original ChromaDB dependent implementation with a
minimal in-memory substitute.  It provides a very small subset of the API used
by the application and the accompanying tests:

``get_or_create_collection`` – obtain a named collection (creating it if it
doesn't exist),
``store_document_chunks`` – persist chunks with embeddings and metadata, and
``search_similar_chunks`` – return stored documents, optionally filtered by the
``document_id`` metadata.

Similarity search is not actually performed; results are simply returned in the
order they were inserted, which is sufficient for unit testing behaviour around
filtering.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class _Collection:
    """Simple container emulating a ChromaDB collection."""

    documents: List[str] = field(default_factory=list)
    embeddings: List[List[float]] = field(default_factory=list)
    metadatas: List[Dict[str, str]] = field(default_factory=list)

    def add(self, *, embeddings, documents, metadatas, ids):  # pragma: no cover - trivial
        self.embeddings.extend(embeddings)
        self.documents.extend(documents)
        self.metadatas.extend(metadatas)

    def query(self, query_embeddings, n_results: int = 5, where: Optional[Dict] = None):
        if where and "document_id" in where:
            docs = [
                doc
                for doc, meta in zip(self.documents, self.metadatas)
                if meta.get("document_id") == where["document_id"]
            ]
        else:
            docs = list(self.documents)
        return {"documents": [docs[:n_results]]}


_collections: Dict[str, _Collection] = {}


def get_or_create_collection(name: str = "iso_documents") -> _Collection:
    """Return a collection with ``name``, creating it on first use."""

    return _collections.setdefault(name, _Collection())


def store_document_chunks(collection: _Collection, chunks: List[str], embeddings, doc_id: str) -> None:
    """Store ``chunks`` and ``embeddings`` within ``collection``."""

    if not chunks or not embeddings:
        return

    metadatas = [{"document_id": doc_id, "chunk_index": i} for i, _ in enumerate(chunks)]
    ids = [str(uuid.uuid4()) for _ in chunks]
    collection.add(embeddings=embeddings, documents=chunks, metadatas=metadatas, ids=ids)


def build_document_filter(doc_id: str) -> Dict[str, str]:
    """Construct a metadata filter for ``doc_id``."""

    return {"document_id": doc_id}


def search_similar_chunks(collection: _Collection, query_embedding, top_k: int = 5, where: Optional[Dict] = None):
    """Return stored documents matching ``where`` criteria.

    No actual vector similarity is computed; this is merely a convenience for
    unit tests that expect the API shape of a similarity search call.
    """

    return collection.query([query_embedding], n_results=top_k, where=where).get("documents", [[]])[0]

