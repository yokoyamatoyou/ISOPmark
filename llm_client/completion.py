from openai import OpenAI
from utils.helpers import load_env_variables
from utils.logger import get_logger

# AGENT.md 4.2.2 APIキー管理
# ヘルパー関数からAPIキーを取得する
env_vars = load_env_variables()
api_key = env_vars["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)
logger = get_logger(__name__)

def get_completion(prompt, model="gpt-4.1-mini"):
    """
    Sends a prompt to the specified GPT model and returns the completion.
    """
    if not prompt:
        return ""

    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,  # 創造性と正確性のバランス
            max_tokens=2048, # 最大出力トークン数
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error("An error occurred while calling the OpenAI API: %s", e, exc_info=True)
        return f"Error: AIモデルの呼び出し中にエラーが発生しました。 {e}"
