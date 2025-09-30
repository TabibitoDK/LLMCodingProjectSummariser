@echo off
TITLE LLM Context Generator Launcher

echo Starting the script...
echo The script is running in this directory:
echo %CD%
echo ---
pause
echo.

echo [Step 1] Checking for the Python script "llm_context_generator.py"...
IF NOT EXIST "llm_context_generator.py" (
    echo [ERROR] The Python script was not found in this directory.
    pause
    exit /b
)
echo [OK] Python script found.
echo ---
pause
echo.

echo --- Entering Step 2 ---
echo [Step 2] Now checking for the virtual environment activation file at:
echo ".\.venv\Scripts\activate.bat"
echo.
IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo [ERROR] The virtual environment file was NOT found at that path.
    echo.
    echo Please make sure you have created a virtual environment named ".venv" in the same folder as this script.
    echo To create it, run this command in your terminal:
    echo python -m venv .venv
    pause
    exit /b
)
echo [OK] Virtual environment activation file found.
echo ---
pause
echo.

echo [Step 3] Activating virtual environment...
CALL .\.venv\Scripts\activate.bat
echo [OK] Activation command sent. If an error occurred, it would be visible above this line.
echo ---
pause
echo.

echo [Step 4] Starting the application...
python llm_context_generator.py

echo.
echo [COMPLETE] The application has closed.
pause

