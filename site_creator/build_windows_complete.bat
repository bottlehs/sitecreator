@echo off
chcp 65001 >nul
title Site Creator - Windows EXE 빌더
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 Site Creator                          ║
echo ║                Windows EXE 빌더 v1.0                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Python 환경 확인
echo 📋 Python 환경 확인 중...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다.
    echo 💡 Python 3.8 이상을 설치해주세요.
    echo 💡 https://python.org 에서 다운로드 가능합니다.
    pause
    exit /b 1
)

echo ✅ Python 환경 확인 완료

REM 가상환경 확인 및 생성
if not exist "venv" (
    echo 🔧 가상환경이 없습니다. 자동으로 생성합니다...
    echo 📦 가상환경 생성 중... (시간이 걸릴 수 있습니다)
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 가상환경 생성에 실패했습니다.
        pause
        exit /b 1
    )
    echo ✅ 가상환경 생성 완료
) else (
    echo ✅ 기존 가상환경 발견
)

REM 가상환경 활성화
echo 🔄 가상환경을 활성화합니다...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 가상환경 활성화에 실패했습니다.
    pause
    exit /b 1
)

REM pip 업그레이드
echo ⬆️ pip를 최신 버전으로 업그레이드합니다...
python -m pip install --upgrade pip

REM 의존성 설치
echo 📦 필요한 패키지들을 설치합니다...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 의존성 설치에 실패했습니다.
    pause
    exit /b 1
)

REM Pillow 설치 (아이콘 생성용)
echo 🎨 아이콘 생성용 Pillow 설치 중...
pip install Pillow

REM PyInstaller 설치
echo 📦 PyInstaller 설치 확인 중...
pip install pyinstaller

REM 아이콘 생성
echo 🎨 Windows용 아이콘 생성 중...
python create_icon.py

REM EXE 파일 생성
echo 🔧 Windows EXE 파일 생성을 시작합니다...
echo ⚠️  이 과정은 5-15분 정도 소요될 수 있습니다.
echo.
python build_windows_only.py

if errorlevel 1 (
    echo.
    echo ❌ EXE 파일 생성에 실패했습니다.
    echo 💡 오류 메시지를 확인하고 문제를 해결해주세요.
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                        🎉 완료!                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📁 생성된 파일 위치: dist\SiteCreator.exe
echo 💡 이 파일을 다른 Windows 컴퓨터에 복사하여 실행할 수 있습니다.
echo 💡 Python 설치 없이도 실행 가능합니다.
echo.
echo 🔍 파일 크기 확인 중...
if exist "dist\SiteCreator.exe" (
    for %%A in ("dist\SiteCreator.exe") do echo 📊 파일 크기: %%~zA bytes
)

echo.
echo 🎊 모든 작업이 완료되었습니다!
pause
