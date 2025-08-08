"""Utility functions for splitting text into overlapping chunks."""


def chunk_text(text, chunk_size: int = 1000, chunk_overlap: int = 200):
    """Split ``text`` into overlapping chunks.

    This simplified implementation avoids heavy third party dependencies
    (e.g. LangChain's ``RecursiveCharacterTextSplitter``) and only relies on
    basic Python operations. Chunks are produced sequentially with the
    specified ``chunk_size`` and an overlap of ``chunk_overlap`` characters
    between consecutive chunks.
    """

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        if end == text_length:
            break
        start = end - chunk_overlap

    return chunks
