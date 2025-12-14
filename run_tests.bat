@echo off
chcp 65001 > nul
cd /d "%~dp0"
env\Scripts\python.exe tests\test_system_integration.py
pause

