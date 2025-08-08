#!/bin/bash

echo "========================================"
echo "ISOP - 仮想環境セットアップ"
echo "========================================"
echo

# Python環境の確認
if ! command -v python3 &> /dev/null; then
    echo "エラー: Python3がインストールされていません"
    echo "Python 3.11以上をインストールしてください"
    exit 1
fi

echo "Python環境を確認しました。"
python3 --version

# 仮想環境の作成
echo
echo "仮想環境を作成しています..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "エラー: 仮想環境の作成に失敗しました"
    exit 1
fi

# 仮想環境の有効化
echo
echo "仮想環境を有効化しています..."
source venv/bin/activate

# pipのアップグレード
echo
echo "pipをアップグレードしています..."
python -m pip install --upgrade pip

# 依存関係のインストール
echo
echo "依存関係をインストールしています..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "エラー: 依存関係のインストールに失敗しました"
    exit 1
fi

echo
echo "========================================"
echo "セットアップが完了しました！"
echo "========================================"
echo
echo "次回からは ./start_isop_venv.sh を使用して起動してください。"
echo
