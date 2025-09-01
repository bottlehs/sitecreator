#!/bin/bash
"""
Python 3.13 가상환경 설정 스크립트 (macOS/Linux)
Site Creator 프로젝트를 Python 3.13에서 실행하기 위한 환경을 구성합니다.
"""

echo "🚀 Site Creator - Python 3.13 환경 설정"
echo "=================================================="

# Python 3.13 설치 확인
echo "🐍 Python 3.13 설치 확인 중..."

# Python 3.13 명령어 확인
PYTHON_CMD=""
if command -v python3.13 &> /dev/null; then
    PYTHON_CMD="python3.13"
    echo "✅ python3.13 명령어 발견"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
    if [[ "$PYTHON_VERSION" == "3.13" ]]; then
        PYTHON_CMD="python3"
        echo "✅ python3 명령어 (버전 3.13) 발견"
    else
        echo "❌ Python 3.13이 설치되어 있지 않습니다."
        echo "현재 버전: $PYTHON_VERSION"
        echo ""
        echo "📦 Python 3.13 설치 방법:"
        echo "1. pyenv 사용 (권장):"
        echo "   pyenv install 3.13.0"
        echo "   pyenv global 3.13.0"
        echo ""
        echo "2. Homebrew 사용 (macOS):"
        echo "   brew install python@3.13"
        echo ""
        echo "3. 공식 웹사이트에서 다운로드:"
        echo "   https://www.python.org/downloads/"
        exit 1
    fi
else
    echo "❌ Python이 설치되어 있지 않습니다."
    exit 1
fi

# Python 버전 재확인
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "📋 사용할 Python: $PYTHON_VERSION"

# 기존 가상환경 백업
if [ -d "venv" ]; then
    echo "📦 기존 가상환경 백업 중..."
    mv venv venv_backup_$(date +%Y%m%d_%H%M%S)
    echo "✅ 백업 완료"
fi

# Python 3.13 가상환경 생성
echo "🔧 Python 3.13 가상환경 생성 중..."
$PYTHON_CMD -m venv venv

if [ $? -eq 0 ]; then
    echo "✅ 가상환경 생성 완료"
else
    echo "❌ 가상환경 생성 실패"
    exit 1
fi

# 가상환경 활성화
echo "🔌 가상환경 활성화 중..."
source venv/bin/activate

# pip 업그레이드
echo "📦 pip 업그레이드 중..."
pip install --upgrade pip

# 의존성 패키지 설치
echo "📚 의존성 패키지 설치 중..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ 모든 패키지 설치 완료"
else
    echo "❌ 패키지 설치 중 오류 발생"
    exit 1
fi

# Python 3.13 호환성 확인
echo "🔍 Python 3.13 호환성 확인 중..."
python check_python_version.py

echo ""
echo "🎉 Python 3.13 환경 설정이 완료되었습니다!"
echo ""
echo "💡 사용 방법:"
echo "1. 가상환경 활성화: source venv/bin/activate"
echo "2. 애플리케이션 실행: python ui.py"
echo "3. 가상환경 비활성화: deactivate"
echo ""
echo "📁 현재 가상환경: $(pwd)/venv"
echo "🐍 Python 버전: $PYTHON_VERSION"
