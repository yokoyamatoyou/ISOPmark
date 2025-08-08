@echo off
echo ========================================
echo ISOP - 規格対応書類更新AIエージェント
echo ========================================
echo.

REM 仮想環境の存在確認
if not exist "venv" (
    echo 仮想環境が見つかりません。
    echo setup_venv.bat を実行して仮想環境を作成してください。
    echo.
    pause
    exit /b 1
)

REM 環境変数の確認
if not defined OPENAI_API_KEY (
    echo 警告: OPENAI_API_KEYが設定されていません
    echo .envファイルを作成するか、環境変数を設定してください
    echo.
)

REM 仮想環境の有効化
echo 仮想環境を有効化しています...
call venv\Scripts\activate.bat

REM Python環境の確認
python --version >nul 2>&1
if errorlevel 1 (
    echo エラー: 仮想環境のPythonが見つかりません
    echo setup_venv.bat を再実行してください
    pause
    exit /b 1
)

echo Python環境を確認しました。
python --version

REM アプリケーションの起動
echo.
echo アプリケーションを起動しています...
echo ブラウザが自動的に開きます
echo.
echo 停止するには Ctrl+C を押してください
echo.

streamlit run app_core/app.py --server.port 8501 --server.address localhost

pause
