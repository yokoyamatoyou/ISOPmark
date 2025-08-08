import io
import logging

"""Utilities for extracting text from common document formats."""

import pypdf

# ``python-docx`` is an optional dependency.  Importing it at module load time
# causes the whole package import to fail when the library is missing.  The
# tests only require graceful handling when the dependency is absent, so the
# import is performed defensively and ``None`` is used as a sentinel value.  The
# actual function will raise a ``ValueError`` if DOCX support is unavailable.
try:  # pragma: no cover - simple dependency check
    import docx  # type: ignore
except Exception:  # pragma: no cover - environment without python-docx
    docx = None

logger = logging.getLogger(__name__)

def extract_text(file_content, file_type):
    """
    Extracts text from a file based on its type.
    """
    if file_type == 'application/pdf':
        return extract_text_from_pdf(file_content)
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return extract_text_from_docx(file_content)
    elif file_type == 'text/plain':
        return extract_text_from_txt(file_content)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def extract_text_from_pdf(file_content):
    """
    Extracts text from a PDF file.
    """
    text = ""
    try:
        pdf_reader = pypdf.PdfReader(io.BytesIO(file_content))
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    except Exception as e:  # pragma: no cover - defensive
        logger.error("Failed to extract text from PDF: %s", e)
        raise ValueError("Failed to extract text from PDF") from e
    return text

def extract_text_from_docx(file_content):
    """
    Extracts text from a DOCX file.
    """
    if docx is None:  # pragma: no cover - simple runtime guard
        raise ValueError("python-docx is required to process DOCX files")

    text = ""
    try:
        doc = docx.Document(io.BytesIO(file_content))
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:  # pragma: no cover - defensive
        logger.error("Failed to extract text from DOCX: %s", e)
        raise ValueError("Failed to extract text from DOCX") from e
    return text

def extract_text_from_txt(file_content):
    """
    Extracts text from a TXT file.
    """
    return file_content.decode('utf-8')

