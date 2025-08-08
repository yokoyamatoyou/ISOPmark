@echo off
echo ========================================
echo ISOP - 規格対応書類更新AIエージェント
echo ========================================
echo.

REM 環境変数の確認
if not defined OPENAI_API_KEY (
    echo 警告: OPENAI_API_KEYが設定されていません
    echo .envファイルを作成するか、環境変数を設定してください
    echo.
)

REM Python環境の確認
python --version >nul 2>&1
if errorlevel 1 (
    echo エラー: Pythonがインストールされていません
    echo Python 3.11以上をインストールしてください
    pause
    exit /b 1
)

REM 依存関係の確認
if not exist "requirements.txt" (
    echo エラー: requirements.txtが見つかりません
    pause
    exit /b 1
)

REM 依存関係のインストール
echo 依存関係をインストールしています...
pip install -r requirements.txt
if errorlevel 1 (
    echo エラー: 依存関係のインストールに失敗しました
    pause
    exit /b 1
)

REM アプリケーションの起動
echo.
echo アプリケーションを起動しています...
echo ブラウザが自動的に開きます
echo.
echo 停止するには Ctrl+C を押してください
echo.

streamlit run app_core/app.py --server.port 8501 --server.address localhost

pause
