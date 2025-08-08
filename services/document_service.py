import uuid  # For generating unique document IDs

from document_processor.extractor import extract_text
from document_processor.chunker import chunk_text
from llm_client.embedding import generate_embeddings
from vector_db_manager.chroma import (
    get_or_create_collection,
    store_document_chunks,
)

from utils.logger import get_logger

logger = get_logger(__name__)

# AGENT.md 9.2.2 services モジュール


def process_and_store_document(file_content, file_type, document_name):
    """
    Orchestrates the entire process of document processing and storage.
    """
    logger.info(f"Starting processing for document: {document_name}")

    # 1. テキスト抽出
    logger.info("Step 1: Extracting text...")
    text = extract_text(file_content, file_type)
    if not text:
        logger.warning("No text extracted. Aborting.")
        return None, 0
    logger.info(
        "Text extracted successfully. Length: "
        f"{len(text)} characters."
    )

    # 2. テキストのチャンク化
    logger.info("Step 2: Chunking text...")
    chunks = chunk_text(text)
    num_chunks = len(chunks)
    logger.info(f"Text chunked into {num_chunks} chunks.")

    # 3. ベクトル埋め込みの生成
    logger.info("Step 3: Generating embeddings...")
    try:
        embeddings = generate_embeddings(chunks)
        if not embeddings:
            logger.error("Failed to generate embeddings. Aborting.")
            return None, 0
        logger.info("Embeddings generated successfully.")
    except Exception as e:
        logger.error(
            f"An error occurred during embedding generation: {e}",
            exc_info=True,
        )
        raise

    # 4. ベクトルデータベースへの格納
    logger.info("Step 4: Storing document in vector database...")
    doc_id = f"doc_{str(uuid.uuid4())}"
    try:
        collection = get_or_create_collection()
        store_document_chunks(collection, chunks, embeddings, doc_id)
        logger.info(f"Document stored successfully with ID: {doc_id}")
    except Exception as e:
        logger.error(
            f"An error occurred during vector DB storage: {e}",
            exc_info=True,
        )
        raise

    return doc_id, num_chunks
