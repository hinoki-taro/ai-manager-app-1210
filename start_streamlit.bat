@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo Starting Streamlit app...
echo Working directory: %CD%
env\Scripts\python.exe -m streamlit run main.py

