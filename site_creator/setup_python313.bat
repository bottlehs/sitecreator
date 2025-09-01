@echo off
REM Python 3.13 가상환경 설정 스크립트 (Windows)
REM Site Creator 프로젝트를 Python 3.13에서 실행하기 위한 환경을 구성합니다.

echo 🚀 Site Creator - Python 3.13 환경 설정
echo ==================================================

REM Python 3.13 설치 확인
echo 🐍 Python 3.13 설치 확인 중...

REM Python 3.13 명령어 확인
set PYTHON_CMD=
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo 📋 Python 버전: %PYTHON_VERSION%
    
    REM 버전에서 3.13 확인
    echo %PYTHON_VERSION% | findstr "3.13" >nul
    if %errorlevel% equ 0 (
        set PYTHON_CMD=python
        echo ✅ Python 3.13 발견
    ) else (
        echo ❌ Python 3.13이 설치되어 있지 않습니다.
        echo 현재 버전: %PYTHON_VERSION%
        echo.
        echo 📦 Python 3.13 설치 방법:
        echo 1. 공식 웹사이트에서 다운로드:
        echo    https://www.python.org/downloads/
        echo 2. Microsoft Store에서 설치:
        echo    Python 3.13 검색 후 설치
        echo.
        pause
        exit /b 1
    )
) else (
    echo ❌ Python이 설치되어 있지 않습니다.
    echo.
    echo 📦 Python 3.13 설치 방법:
    echo 1. 공식 웹사이트에서 다운로드:
    echo    https://www.python.org/downloads/
    echo 2. Microsoft Store에서 설치:
    echo    Python 3.13 검색 후 설치
    echo.
    pause
    exit /b 1
)

REM 기존 가상환경 백업
if exist "venv" (
    echo 📦 기존 가상환경 백업 중...
    set BACKUP_NAME=venv_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    set BACKUP_NAME=%BACKUP_NAME: =0%
    ren venv %BACKUP_NAME%
    echo ✅ 백업 완료: %BACKUP_NAME%
)

REM Python 3.13 가상환경 생성
echo 🔧 Python 3.13 가상환경 생성 중...
%PYTHON_CMD% -m venv venv

if %errorlevel% equ 0 (
    echo ✅ 가상환경 생성 완료
) else (
    echo ❌ 가상환경 생성 실패
    pause
    exit /b 1
)

REM 가상환경 활성화
echo 🔌 가상환경 활성화 중...
call venv\Scripts\activate.bat

REM pip 업그레이드
echo 📦 pip 업그레이드 중...
python -m pip install --upgrade pip

REM 의존성 패키지 설치
echo 📚 의존성 패키지 설치 중...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo ✅ 모든 패키지 설치 완료
) else (
    echo ❌ 패키지 설치 중 오류 발생
    pause
    exit /b 1
)

REM Python 3.13 호환성 확인
echo 🔍 Python 3.13 호환성 확인 중...
python check_python_version.py

echo.
echo 🎉 Python 3.13 환경 설정이 완료되었습니다!
echo.
echo 💡 사용 방법:
echo 1. 가상환경 활성화: venv\Scripts\activate.bat
echo 2. 애플리케이션 실행: python ui.py
echo 3. 가상환경 비활성화: deactivate
echo.
echo 📁 현재 가상환경: %cd%\venv
echo 🐍 Python 버전: %PYTHON_VERSION%
echo.
pause
