@echo off
chcp 65001 >nul
echo 🚀 Site Creator - Windows EXE 빌더
echo ================================================

REM Python 환경 확인
echo 📋 Python 환경 확인 중...
python --version
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다.
    echo 💡 Python 3.8 이상을 설치해주세요.
    pause
    exit /b 1
)

REM 가상환경 활성화 확인
if not exist "venv" (
    echo 🔧 가상환경이 없습니다. 자동으로 생성합니다...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 가상환경 생성에 실패했습니다.
        pause
        exit /b 1
    )
)

REM 가상환경 활성화
echo ✅ 가상환경을 활성화합니다...
call venv\Scripts\activate.bat

REM pip 업그레이드
echo ⬆️ pip를 최신 버전으로 업그레이드합니다...
python -m pip install --upgrade pip

REM 의존성 설치
echo 📦 필요한 패키지들을 설치합니다...
pip install -r requirements.txt

REM PyInstaller 설치 확인
echo 📦 PyInstaller 설치 확인 중...
pip install pyinstaller

REM exe 파일 생성
echo 🔧 Windows EXE 파일 생성을 시작합니다...
python build_windows_only.py

echo.
echo 🎊 빌드 프로세스가 완료되었습니다!
echo 📁 dist 폴더를 확인하여 SiteCreator.exe 파일을 찾으세요.
echo 💡 이 파일을 다른 Windows 컴퓨터에 복사하여 실행할 수 있습니다.
echo 💡 파일 크기는 약 50-100MB 정도입니다.

pause
