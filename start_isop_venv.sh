#!/bin/bash

echo "========================================"
echo "ISOP - 規格対応書類更新AIエージェント"
echo "========================================"
echo

# 仮想環境の存在確認
if [ ! -d "venv" ]; then
    echo "仮想環境が見つかりません。"
    echo "./setup_venv.sh を実行して仮想環境を作成してください。"
    echo
    exit 1
fi

# 環境変数の確認
if [ -z "$OPENAI_API_KEY" ]; then
    echo "警告: OPENAI_API_KEYが設定されていません"
    echo ".envファイルを作成するか、環境変数を設定してください"
    echo
fi

# 仮想環境の有効化
echo "仮想環境を有効化しています..."
source venv/bin/activate

# Python環境の確認
if ! command -v python &> /dev/null; then
    echo "エラー: 仮想環境のPythonが見つかりません"
    echo "./setup_venv.sh を再実行してください"
    exit 1
fi

echo "Python環境を確認しました。"
python --version

# アプリケーションの起動
echo
echo "アプリケーションを起動しています..."
echo "ブラウザが自動的に開きます"
echo
echo "停止するには Ctrl+C を押してください"
echo

streamlit run app_core/app.py --server.port 8501 --server.address localhost
