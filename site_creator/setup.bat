@echo off
echo 🚀 Site Creator 프로젝트 설정을 시작합니다...

REM Python 버전 확인
echo 📋 Python 버전 확인 중...
python --version

REM 기존 가상환경이 있다면 삭제
if exist "venv" (
    echo 🗑️  기존 가상환경을 삭제합니다...
    rmdir /s /q venv
)

REM 새 가상환경 생성
echo 🔧 새로운 가상환경을 생성합니다...
python -m venv venv

REM 가상환경 활성화
echo ✅ 가상환경을 활성화합니다...
call venv\Scripts\activate.bat

REM pip 업그레이드
echo ⬆️  pip를 최신 버전으로 업그레이드합니다...
python -m pip install --upgrade pip

REM 의존성 설치
echo 📦 필요한 패키지들을 설치합니다...
pip install -r requirements.txt

echo 🎉 설치가 완료되었습니다!
echo.
echo 다음 명령어로 애플리케이션을 실행할 수 있습니다:
echo venv\Scripts\activate
echo python ui.py
echo.
echo 또는 한 번에 실행:
echo venv\Scripts\activate.bat && python ui.py

pause
