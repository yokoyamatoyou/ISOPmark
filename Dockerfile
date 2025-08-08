# Python 3.11をベースイメージとして使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコンテナにコピー
# まずは依存関係ファイルからコピーして、キャッシュを有効活用する
COPY requirements.txt .

# 依存関係をインストール
# requirements.txtがまだないので、ここでライブラリを直接インストール
RUN pip install --no-cache-dir streamlit pypdf python-docx langchain openai chromadb python-dotenv

# アプリケーションのソースコードをコピー
COPY . .

# 環境変数としてOpenAI APIキーを設定（ビルド時に渡すか、実行時に設定）
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Streamlitが使用するポートを公開
EXPOSE 8501

# アプリケーションのヘルスチェック
HEALTHCHECK CMD streamlit hello

# コンテナ起動時にStreamlitアプリケーションを実行
CMD ["streamlit", "run", "app_core/app.py"] 
