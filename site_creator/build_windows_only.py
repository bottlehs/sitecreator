#!/usr/bin/env python3
"""
Site Creator - Windows 전용 exe 빌더
Windows에서만 실행되어야 합니다.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_windows():
    """Windows 환경 확인"""
    if platform.system() != "Windows":
        print("❌ 이 스크립트는 Windows에서만 실행할 수 있습니다.")
        print(f"현재 OS: {platform.system()}")
        print("💡 Windows 컴퓨터에서 이 스크립트를 실행해주세요.")
        return False
    print("✅ Windows 환경 확인 완료")
    return True

def check_pyinstaller():
    """PyInstaller 설치 확인 및 설치"""
    try:
        import PyInstaller
        print("✅ PyInstaller가 이미 설치되어 있습니다.")
        return True
    except ImportError:
        print("📦 PyInstaller를 설치합니다...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller 설치 완료!")
            return True
        except subprocess.CalledProcessError:
            print("❌ PyInstaller 설치 실패!")
            return False

def create_windows_exe():
    """Windows exe 파일 생성"""
    print("🔧 Windows exe 파일 생성을 시작합니다...")
    
    # 현재 디렉토리 확인
    current_dir = Path.cwd()
    ui_file = current_dir / "ui.py"
    
    if not ui_file.exists():
        print(f"❌ ui.py 파일을 찾을 수 없습니다: {ui_file}")
        return False
    
    # Windows용 PyInstaller 명령어 구성
    cmd = [
        "pyinstaller",
        "--onefile",                    # 단일 exe 파일 생성
        "--windowed",                   # 콘솔 창 숨김
        "--name=SiteCreator",           # exe 파일명
        "--icon=icon.ico",              # 아이콘 (있는 경우)
        "--add-data=page_default;page_default",  # Flask 앱 포함 (Windows 구분자)
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=paramiko",
        "--hidden-import=flask",
        "--hidden-import=bs4",
        "--hidden-import=user_agents",
        "--clean",                       # 빌드 캐시 정리
        "--noconfirm",                   # 기존 파일 덮어쓰기
        "--version-file=version_info.txt",  # 버전 정보 포함
        str(ui_file)
    ]
    
    # 아이콘이 없으면 제거
    if not (current_dir / "icon.ico").exists():
        cmd.remove("--icon=icon.ico")
        print("⚠️  icon.ico 파일이 없습니다. 기본 아이콘을 사용합니다.")
    
    print("📋 PyInstaller 명령어:")
    print(" ".join(cmd))
    print()
    
    try:
        # PyInstaller 실행
        print("🚀 Windows exe 파일 생성 중... (시간이 걸릴 수 있습니다)")
        subprocess.check_call(cmd)
        
        # 결과 확인
        dist_dir = current_dir / "dist"
        exe_file = dist_dir / "SiteCreator.exe"
        
        if exe_file.exists():
            print(f"✅ Windows exe 파일 생성 완료: {exe_file}")
            print(f"📁 파일 크기: {exe_file.stat().st_size / (1024*1024):.1f} MB")
            
            # 사용자에게 안내
            print("\n🎉 Windows exe 파일이 성공적으로 생성되었습니다!")
            print(f"📂 위치: {exe_file}")
            print("💡 이제 Windows에서 SiteCreator.exe를 더블클릭하여 실행할 수 있습니다.")
            
            return True
        else:
            print("❌ Windows exe 파일 생성 실패!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows exe 파일 생성 중 오류 발생: {e}")
        return False

def main():
    """메인 함수"""
    print("🚀 Site Creator - Windows 전용 빌더")
    print("=" * 50)
    
    # Windows 환경 확인
    if not check_windows():
        return
    
    # PyInstaller 확인
    if not check_pyinstaller():
        return
    
    # Windows exe 파일 생성
    if create_windows_exe():
        print("\n🎊 Windows 빌드 완료!")
        print("📁 dist 폴더에 SiteCreator.exe 파일이 생성되었습니다.")
        print("💡 이 파일을 다른 Windows 컴퓨터에 복사하여 실행할 수 있습니다.")
    else:
        print("❌ Windows exe 파일 생성에 실패했습니다.")

if __name__ == "__main__":
    main()
