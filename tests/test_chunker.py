from document_processor.chunker import chunk_text


def test_chunk_text():
    text = "a" * 1000 + "b" * 1000 + "c" * 1000
    chunks = chunk_text(text, chunk_size=1000, chunk_overlap=200)
    assert len(chunks) == 4
    for i in range(len(chunks) - 1):
        assert chunks[i][-200:] == chunks[i + 1][:200]

