#!/usr/bin/env python3
"""
Python 3.13 호환성 확인 스크립트
Site Creator 프로젝트가 Python 3.13에서 정상 작동하는지 확인합니다.
"""

import sys
import platform
import subprocess
from pathlib import Path

def check_python_version():
    """Python 버전 확인"""
    print("🐍 Python 버전 확인")
    print("=" * 50)
    
    # 현재 Python 버전
    current_version = sys.version_info
    print(f"현재 Python 버전: {current_version.major}.{current_version.minor}.{current_version.micro}")
    print(f"Python 실행 경로: {sys.executable}")
    print(f"플랫폼: {platform.system()} {platform.release()}")
    
    # Python 3.13 이상 확인
    if current_version >= (3, 13):
        print("✅ Python 3.13+ 호환성 확인됨")
        return True
    else:
        print("❌ Python 3.13 이상이 필요합니다.")
        print(f"   현재: {current_version.major}.{current_version.minor}.{current_version.micro}")
        print("   필요: 3.13+")
        return False

def check_required_packages():
    """필수 패키지 설치 확인"""
    print("\n📦 필수 패키지 확인")
    print("=" * 50)
    
    required_packages = [
        'PyQt5',
        'Flask',
        'paramiko',
        'beautifulsoup4',
        'lxml',
        'user_agents',
        'requests',
        'watchdog',
        'gunicorn'
    ]
    
    missing_packages = []
    installed_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
            installed_packages.append(package)
        except ImportError:
            print(f"❌ {package} (설치 필요)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  설치가 필요한 패키지: {', '.join(missing_packages)}")
        print("다음 명령어로 설치하세요:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    else:
        print(f"\n✅ 모든 필수 패키지가 설치되어 있습니다.")
        return True

def check_pyinstaller():
    """PyInstaller 확인"""
    print("\n🔧 PyInstaller 확인")
    print("=" * 50)
    
    try:
        import PyInstaller
        version = PyInstaller.__version__
        print(f"✅ PyInstaller {version}")
        
        # Python 3.13 호환성을 위해 6.0.0+ 권장
        if tuple(map(int, version.split('.'))) >= (6, 0, 0):
            print("✅ Python 3.13 호환 버전")
        else:
            print("⚠️  Python 3.13 호환성을 위해 PyInstaller 6.0.0+ 업그레이드 권장")
            print("   pip install --upgrade pyinstaller")
        
        return True
    except ImportError:
        print("❌ PyInstaller가 설치되어 있지 않습니다.")
        print("   pip install pyinstaller")
        return False

def create_python313_venv():
    """Python 3.13 가상환경 생성 가이드"""
    print("\n🔧 Python 3.13 가상환경 생성 가이드")
    print("=" * 50)
    
    if platform.system() == "Windows":
        print("Windows에서 Python 3.13 가상환경 생성:")
        print("1. Python 3.13 설치 (python.org에서 다운로드)")
        print("2. 명령 프롬프트에서:")
        print("   python -m venv venv_py313")
        print("   venv_py313\\Scripts\\activate")
        print("   pip install -r requirements.txt")
    else:
        print("macOS/Linux에서 Python 3.13 가상환경 생성:")
        print("1. Python 3.13 설치 (pyenv 또는 시스템 패키지 매니저)")
        print("2. 터미널에서:")
        print("   python3.13 -m venv venv_py313")
        print("   source venv_py313/bin/activate")
        print("   pip install -r requirements.txt")

def main():
    """메인 함수"""
    print("🚀 Site Creator - Python 3.13 호환성 확인")
    print("=" * 60)
    
    # Python 버전 확인
    version_ok = check_python_version()
    
    # 패키지 확인
    packages_ok = check_required_packages()
    
    # PyInstaller 확인
    pyinstaller_ok = check_pyinstaller()
    
    # 결과 요약
    print("\n📊 호환성 확인 결과")
    print("=" * 50)
    
    if version_ok and packages_ok and pyinstaller_ok:
        print("🎉 모든 호환성 검사를 통과했습니다!")
        print("Site Creator를 Python 3.13에서 실행할 수 있습니다.")
    else:
        print("⚠️  일부 호환성 검사에 실패했습니다.")
        if not version_ok:
            print("   - Python 3.13+ 설치 필요")
        if not packages_ok:
            print("   - 필수 패키지 설치 필요")
        if not pyinstaller_ok:
            print("   - PyInstaller 설치 필요")
    
    # 가상환경 생성 가이드
    if not version_ok:
        create_python313_venv()
    
    print("\n💡 추가 도움이 필요하면 README.md를 참조하세요.")

if __name__ == "__main__":
    main()
