import io
import pytest

from document_processor.extractor import extract_text

def create_pdf_bytes(text: str) -> bytes:
    from reportlab.pdfgen import canvas

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, text)
    c.save()
    return buffer.getvalue()

def create_docx_bytes(text: str) -> bytes:
    from docx import Document

    buffer = io.BytesIO()
    doc = Document()
    doc.add_paragraph(text)
    doc.save(buffer)
    return buffer.getvalue()

def test_extract_text_pdf():
    content = create_pdf_bytes("Hello, PDF!")
    text = extract_text(content, "application/pdf")
    assert text.strip() == "Hello, PDF!"

def test_extract_text_docx():
    content = create_docx_bytes("Hello, DOCX!")
    text = extract_text(
        content,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    assert text.strip() == "Hello, DOCX!"

def test_extract_text_txt():
    content = "Hello, TXT!".encode("utf-8")
    text = extract_text(content, "text/plain")
    assert text == "Hello, TXT!"


def test_extract_text_pdf_error():
    corrupted_pdf = b"corrupted pdf data"
    with pytest.raises(ValueError):
        extract_text(corrupted_pdf, "application/pdf")


def test_extract_text_docx_error():
    corrupted_docx = b"not a docx file"
    with pytest.raises(ValueError):
        extract_text(
            corrupted_docx,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
