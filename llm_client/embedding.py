from openai import OpenAI
from utils.helpers import load_env_variables
from utils.logger import get_logger

# AGENT.md 4.2.2 APIキー管理
# ヘルパー関数からAPIキーを取得する
env_vars = load_env_variables()
api_key = env_vars["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)
logger = get_logger(__name__)

def generate_embeddings(text_chunks, model="text-embedding-3-small"):
    """
    Generates vector embeddings for a list of text chunks using OpenAI's API.
    """
    if not text_chunks:
        return []

    try:
        # OpenAIのAPIはリスト形式でテキストを受け取る
        response = client.embeddings.create(input=text_chunks, model=model)
        # 埋め込みデータを抽出して返す
        return [embedding.embedding for embedding in response.data]
    except Exception as e:
        logger.error(
            "An error occurred while generating embeddings: %s", e, exc_info=True
        )
        return []
