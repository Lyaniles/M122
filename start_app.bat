@echo off
echo Starting Gemini Google Scraper...

:: Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo Checking dependencies...
pip install -r requirements.txt --quiet

:: Run the app
echo Launching application...
python -m streamlit run app.py
pause