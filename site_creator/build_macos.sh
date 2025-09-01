#!/bin/bash
echo "🚀 Site Creator - macOS DMG 빌더"
echo "================================================"

# 가상환경 활성화 확인
if [ ! -d "venv" ]; then
    echo "❌ 가상환경이 없습니다. 먼저 setup.sh를 실행해주세요."
    exit 1
fi

# 가상환경 활성화
echo "✅ 가상환경을 활성화합니다..."
source venv/bin/activate

# PyInstaller 설치 확인
echo "📦 PyInstaller 설치 확인 중..."
pip install pyinstaller

# macOS 앱 및 DMG 생성
echo "🔧 macOS 앱 및 DMG 생성을 시작합니다..."
python build_macos.py

echo ""
echo "🎊 macOS 빌드 프로세스가 완료되었습니다!"
echo "📁 dist 폴더와 SiteCreator_macOS.dmg 파일을 확인하세요."
echo "💡 DMG 파일을 더블클릭하여 앱을 설치할 수 있습니다."
