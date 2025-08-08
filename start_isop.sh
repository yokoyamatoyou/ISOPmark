#!/bin/bash

echo "========================================"
echo "ISOP - 規格対応書類更新AIエージェント"
echo "========================================"
echo

# 環境変数の確認
if [ -z "$OPENAI_API_KEY" ]; then
    echo "警告: OPENAI_API_KEYが設定されていません"
    echo ".envファイルを作成するか、環境変数を設定してください"
    echo
fi

# Python環境の確認
if ! command -v python3 &> /dev/null; then
    echo "エラー: Python3がインストールされていません"
    echo "Python 3.11以上をインストールしてください"
    exit 1
fi

# 依存関係の確認
if [ ! -f "requirements.txt" ]; then
    echo "エラー: requirements.txtが見つかりません"
    exit 1
fi

# 依存関係のインストール
echo "依存関係をインストールしています..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "エラー: 依存関係のインストールに失敗しました"
    exit 1
fi

# アプリケーションの起動
echo
echo "アプリケーションを起動しています..."
echo "ブラウザが自動的に開きます"
echo
echo "停止するには Ctrl+C を押してください"
echo

streamlit run app_core/app.py --server.port 8501 --server.address localhost
