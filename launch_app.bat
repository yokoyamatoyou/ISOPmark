@echo off
rem Change directory to the script's location
cd /d "%~dp0"

echo Starting Streamlit application...

rem Execute streamlit run command
streamlit run app_core\app.py --server.headless true
