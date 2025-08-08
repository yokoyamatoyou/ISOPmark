@echo off
rem バッチファイルがあるディレクトリに移動します
cd /d "%~dp0"

echo Starting the AI Document Updater application...

rem Pythonスクリプトを実行してStreamlitを起動します
python run_app.py

echo Application process has been started.

pause
