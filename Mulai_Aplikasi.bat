@echo off
cd /d "%~dp0"
title Aquascape Fuzzy - Web App
color 0A

echo ========================================================
echo Memulai Aquascape Fuzzy Application (Web UI)
echo ========================================================
echo.

:: 1. Cek instalasi python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak terdeteksi di sistem ini.
    echo Silakan install Python ^(minimal versi 3.9^) dari python.org
    echo dan pastikan opsi "Add Python to PATH" dicentang saat instalasi.
    echo.
    pause
    exit
)
echo [OK] Python terdeteksi.

:: 2. Buat virtual environment jika belum ada
if not exist venv (
    echo [INFO] Virtual environment belum ada. Membuat venv baru...
    python -m venv venv
    echo [OK] Virtual environment berhasil dibuat.
) else (
    echo [OK] Virtual environment sudah ada.
)

:: 3. Aktifkan virtual environment
echo [INFO] Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

:: 4. Install/update dependencies
echo [INFO] Mengecek dan menginstall dependencies dari requirements.txt...
pip install -r requirements.txt
echo [OK] Dependencies siap.
echo.

:: 5. Jalankan aplikasi
echo ========================================================
echo Menjalankan aplikasi web... (Streamlit)
echo Browser akan otomatis terbuka. Jika tidak, buka URL yang tertera di bawah.
echo ========================================================
streamlit run app.py

pause
