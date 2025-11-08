@echo off
REM سكريبت لتشغيل تطبيق Twitter Sentiment Analyzer على Windows

echo Starting Twitter Sentiment Analyzer...
echo.

REM التحقق من ملف .env
if not exist .env (
    echo Error: .env file not found!
    echo Please copy .env.example to .env and add your Twitter API keys
    echo.
    echo Run:
    echo   copy .env.example .env
    echo   notepad .env
    pause
    exit /b 1
)

REM تشغيل Streamlit
streamlit run app.py

pause
