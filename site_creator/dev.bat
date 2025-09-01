@echo off
echo 🔧 Site Creator 개발 모드 실행
echo ================================

REM 가상환경 활성화 확인
if not exist "venv" (
    echo ❌ 가상환경이 없습니다. 먼저 setup.bat를 실행해주세요.
    pause
    exit /b 1
)

REM 가상환경 활성화
echo ✅ 가상환경을 활성화합니다...
call venv\Scripts\activate.bat

REM watchdog 패키지 설치 확인
echo 📦 watchdog 패키지 설치 확인 중...
pip install watchdog

REM 개발 모드 실행
echo 🚀 개발 모드를 시작합니다...
echo 💡 파일을 수정하면 자동으로 애플리케이션이 재시작됩니다.
echo 💡 종료하려면 Ctrl+C를 누르세요.
echo ================================

python dev_run.py

pause
