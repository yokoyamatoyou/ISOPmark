@echo off
echo ========================================
echo ISOP - 仮想環境セットアップ
echo ========================================
echo.

REM Python環境の確認
python --version >nul 2>&1
if errorlevel 1 (
    echo エラー: Pythonがインストールされていません
    echo Python 3.11以上をインストールしてください
    pause
    exit /b 1
)

echo Python環境を確認しました。
python --version

REM 仮想環境の作成
echo.
echo 仮想環境を作成しています...
python -m venv venv
if errorlevel 1 (
    echo エラー: 仮想環境の作成に失敗しました
    pause
    exit /b 1
)

REM 仮想環境の有効化
echo.
echo 仮想環境を有効化しています...
call venv\Scripts\activate.bat

REM pipのアップグレード
echo.
echo pipをアップグレードしています...
python -m pip install --upgrade pip

REM 依存関係のインストール
echo.
echo 依存関係をインストールしています...
pip install -r requirements.txt
if errorlevel 1 (
    echo エラー: 依存関係のインストールに失敗しました
    pause
    exit /b 1
)

echo.
echo ========================================
echo セットアップが完了しました！
echo ========================================
echo.
echo 次回からは start_isop_venv.bat を使用して起動してください。
echo.
pause
