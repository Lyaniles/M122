@echo off
echo Starting Lead Generation Scraper...

:: Check if the specific activate script exists. 
:: If not, the venv is missing or broken, so we (re)create it.
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Check if activation worked
if %errorlevel% neq 0 (
    echo Error: Could not activate virtual environment.
    pause
    exit /b
)

:: Install dependencies
echo Checking dependencies...
pip install -r requirements.txt --quiet

:: Run the app
echo Launching application...
python -m streamlit run app.py
pause
