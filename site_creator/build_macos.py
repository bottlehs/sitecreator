#!/usr/bin/env python3
"""
Site Creator - macOS DMG 파일 빌드 스크립트
PyInstaller를 사용하여 macOS 앱 번들 생성 후 DMG로 패키징
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import platform

def check_macos():
    """macOS 환경 확인"""
    if platform.system() != "Darwin":
        print("❌ 이 스크립트는 macOS에서만 실행할 수 있습니다.")
        print(f"현재 OS: {platform.system()}")
        return False
    print("✅ macOS 환경 확인 완료")
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

def create_macos_app():
    """macOS 앱 번들 생성"""
    print("🔧 macOS 앱 번들 생성을 시작합니다...")
    
    # 현재 디렉토리 확인
    current_dir = Path.cwd()
    ui_file = current_dir / "ui.py"
    
    if not ui_file.exists():
        print(f"❌ ui.py 파일을 찾을 수 없습니다: {ui_file}")
        return False
    
    # PyInstaller 명령어 구성 (macOS용)
    cmd = [
        "pyinstaller",
        "--onedir",                     # 디렉토리 모드 (macOS 권장)
        "--windowed",                   # GUI 모드 (콘솔 창 숨김)
        "--name=SiteCreator",           # 앱 이름
        "--icon=icon.icns",             # macOS 아이콘 (있는 경우)
        "--add-data=page_default:page_default",  # Flask 앱 포함 (macOS 구분자)
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=paramiko",
        "--hidden-import=flask",
        "--hidden-import=bs4",
        "--hidden-import=user_agents",
        "--clean",                       # 빌드 캐시 정리
        "--noconfirm",                   # 기존 파일 덮어쓰기
        str(ui_file)
    ]
    
    # 아이콘이 없으면 제거
    if not (current_dir / "icon.icns").exists():
        cmd.remove("--icon=icon.icns")
        print("⚠️  icon.icns 파일이 없습니다. 기본 아이콘을 사용합니다.")
    
    print("📋 PyInstaller 명령어:")
    print(" ".join(cmd))
    print()
    
    try:
        # PyInstaller 실행
        print("🚀 macOS 앱 번들 생성 중... (시간이 걸릴 수 있습니다)")
        subprocess.check_call(cmd)
        
        # 결과 확인
        dist_dir = current_dir / "dist"
        app_file = dist_dir / "SiteCreator"
        
        if app_file.exists():
            print(f"✅ macOS 앱 생성 완료: {app_file}")
            print(f"📁 파일 크기: {app_file.stat().st_size / (1024*1024):.1f} MB")
            return True
        else:
            print("❌ macOS 앱 생성 실패!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ macOS 앱 생성 중 오류 발생: {e}")
        return False

def create_dmg():
    """DMG 파일 생성"""
    print("🔧 DMG 파일 생성을 시작합니다...")
    
    current_dir = Path.cwd()
    dist_dir = current_dir / "dist"
    sitecreator_dir = dist_dir / "SiteCreator"
    
    if not sitecreator_dir.exists():
        print("❌ SiteCreator 디렉토리가 생성되지 않았습니다.")
        return False
    
    # DMG 생성 명령어
    dmg_name = "SiteCreator_macOS.dmg"
    dmg_path = current_dir / dmg_name
    
    # 기존 DMG 파일이 있다면 삭제
    if dmg_path.exists():
        dmg_path.unlink()
        print("🗑️  기존 DMG 파일을 삭제했습니다.")
    
    # hdiutil을 사용하여 DMG 생성
    try:
        cmd = [
            "hdiutil", "create",
            "-volname", "Site Creator",
            "-srcfolder", str(dist_dir),
            "-ov",  # 덮어쓰기
            str(dmg_path)
        ]
        
        print("📋 DMG 생성 명령어:")
        print(" ".join(cmd))
        print()
        
        print("🚀 DMG 파일 생성 중...")
        subprocess.check_call(cmd)
        
        if dmg_path.exists():
            print(f"✅ DMG 파일 생성 완료: {dmg_path}")
            print(f"📁 파일 크기: {dmg_path.stat().st_size / (1024*1024):.1f} MB")
            
            # DMG 정보 출력
            print("\n📊 DMG 파일 정보:")
            subprocess.run(["hdiutil", "info", str(dmg_path)])
            
            return True
        else:
            print("❌ DMG 파일 생성 실패!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ DMG 파일 생성 중 오류 발생: {e}")
        return False

def create_app_bundle():
    """macOS 앱 번들 (.app) 생성"""
    print("🔧 macOS 앱 번들 (.app) 생성을 시작합니다...")
    
    current_dir = Path.cwd()
    dist_dir = current_dir / "dist"
    sitecreator_dir = dist_dir / "SiteCreator"
    
    if not sitecreator_dir.exists():
        print("❌ SiteCreator 디렉토리가 생성되지 않았습니다.")
        return False
    
    # 앱 번들 디렉토리 생성
    app_bundle_dir = dist_dir / "SiteCreator.app"
    contents_dir = app_bundle_dir / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"
    
    # 디렉토리 구조 생성
    macos_dir.mkdir(parents=True, exist_ok=True)
    resources_dir.mkdir(parents=True, exist_ok=True)
    
    # Info.plist 생성
    info_plist = contents_dir / "Info.plist"
    info_plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>SiteCreator</string>
    <key>CFBundleIdentifier</key>
    <string>com.sitecreator.app</string>
    <key>CFBundleName</key>
    <string>Site Creator</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>'''
    
    info_plist.write_text(info_plist_content)
    
    # 실행 파일을 MacOS 디렉토리로 복사
    main_executable = sitecreator_dir / "SiteCreator"
    if main_executable.exists():
        shutil.copy2(main_executable, macos_dir / "SiteCreator")
        # 실행 권한 부여
        os.chmod(macos_dir / "SiteCreator", 0o755)
    else:
        print("⚠️  SiteCreator 실행 파일을 찾을 수 없습니다.")
        return False
    
    print(f"✅ macOS 앱 번들 생성 완료: {app_bundle_dir}")
    return True

def main():
    """메인 함수"""
    print("🚀 Site Creator - macOS 빌더")
    print("=" * 50)
    
    # macOS 환경 확인
    if not check_macos():
        return
    
    # PyInstaller 확인
    if not check_pyinstaller():
        return
    
    # macOS 앱 생성
    if create_macos_app():
        # 앱 번들 생성
        create_app_bundle()
        
        # DMG 파일 생성
        if create_dmg():
            print("\n🎊 macOS 빌드 완료!")
            print("📁 생성된 파일들:")
            print(f"  - 실행 파일: dist/SiteCreator")
            print(f"  - 앱 번들: dist/SiteCreator.app")
            print(f"  - DMG 파일: SiteCreator_macOS.dmg")
            print("\n💡 DMG 파일을 더블클릭하여 앱을 설치할 수 있습니다.")
        else:
            print("❌ DMG 파일 생성에 실패했습니다.")
    else:
        print("❌ macOS 앱 생성에 실패했습니다.")

if __name__ == "__main__":
    main()
