from vector_db_manager.chroma import (
    get_or_create_collection,
    search_similar_chunks,
    build_document_filter,
)
from llm_client.embedding import generate_embeddings
from llm_client.completion import get_completion
from utils.logger import get_logger

logger = get_logger(__name__)

def rewrite_document_with_rag(existing_doc_id, new_standard_text):
    """
    Rewrites a document using the RAG (Retrieval Augmented Generation) approach.
    """
    logger.info("Starting document rewrite process with RAG...")

    # 1. 新規格のテキストをベクトル化してクエリとして使用
    logger.info("Step 1: Generating embedding for the new standard...")
    try:
        embeddings = generate_embeddings([new_standard_text])
        if not embeddings:
            logger.error("Could not generate embedding for the new standard.")
            return "Error: Could not generate embedding for the new standard."

        query_embedding = embeddings[0]
        if not query_embedding:
            logger.error("Could not generate embedding for the new standard.")
            return "Error: Could not generate embedding for the new standard."
    except Exception as e:
        logger.error(f"Error generating embedding for new standard: {e}", exc_info=True)
        return f"Error: 新規格のベクトル化中にエラーが発生しました。 {e}"

    # 2. 関連する既存文書のチャンクをベクトルDBから検索
    logger.info("Step 2: Searching for relevant chunks from the existing document...")
    try:
        collection = get_or_create_collection()
        retrieved_chunks = search_similar_chunks(
            collection,
            query_embedding,
            top_k=5,
            where=build_document_filter(existing_doc_id),
        )
        if not retrieved_chunks:
            logger.warning("No relevant chunks found. Proceeding without context from existing doc.")
            retrieved_context = "関連する既存の文書情報は見つかりませんでした。"
        else:
            retrieved_context = "\n\n---\n\n".join(retrieved_chunks)
            logger.info(f"Found {len(retrieved_chunks)} relevant chunks.")
    except Exception as e:
        logger.error(f"Error searching for similar chunks: {e}", exc_info=True)
        return f"Error: 関連文書の検索中にエラーが発生しました。 {e}"

    # 3. AIへのプロンプトを構築
    logger.info("Step 3: Constructing prompt for the AI...")
    prompt = f"""
    あなたは、企業のISO規格担当者です。
    以下の新しい規格内容と、それに関連する既存の社内文書の抜粋を参考にして、
    既存の文書を新しい規格に適合するように書き換えてください。

    # 新しい規格内容:
    {new_standard_text}

    # 既存の社内文書からの関連抜粋:
    {retrieved_context}

    # 指示:
    - 上記の情報を基に、既存の文書を全面的に見直し、新しい規格に準拠した内容のマークダウン形式の文書を生成してください。
    - 変更点だけでなく、文書全体を出力してください。
    - AIの判断だけでは対応が難しい、あるいは解釈の確認が必要な項目があれば、`[要確認]`というプレフィックスを付けてその項目を記述してください。
    """

    # 4. AIを呼び出して書き換え後のコンテンツを取得
    logger.info("Step 4: Calling AI for document generation...")
    rewritten_content = get_completion(prompt)
    logger.info("Document generation complete.")

    return rewritten_content

