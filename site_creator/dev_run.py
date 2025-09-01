#!/usr/bin/env python3
"""
Site Creator 개발용 자동 재실행 스크립트
파일 변경을 감지하여 자동으로 애플리케이션을 재시작합니다.
"""

import os
import sys
import time
import subprocess
import signal
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AppRestartHandler(FileSystemEventHandler):
    def __init__(self, app_path):
        self.app_path = app_path
        self.process = None
        self.restart_pending = False
        self.start_app()
    
    def start_app(self):
        """애플리케이션 시작"""
        if self.process:
            self.stop_app()
        
        print(f"🚀 애플리케이션 시작 중... ({time.strftime('%H:%M:%S')})")
        try:
            self.process = subprocess.Popen([sys.executable, self.app_path])
            print(f"✅ 애플리케이션이 시작되었습니다. (PID: {self.process.pid})")
        except Exception as e:
            print(f"❌ 애플리케이션 시작 실패: {e}")
    
    def stop_app(self):
        """애플리케이션 종료"""
        if self.process:
            print(f"🛑 애플리케이션 종료 중... ({time.strftime('%H:%M:%S')})")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                print("✅ 애플리케이션이 종료되었습니다.")
            except subprocess.TimeoutExpired:
                print("⚠️ 강제 종료 중...")
                self.process.kill()
            except Exception as e:
                print(f"❌ 애플리케이션 종료 중 오류: {e}")
            finally:
                self.process = None
    
    def on_modified(self, event):
        """파일 변경 감지"""
        if event.is_directory:
            return
        
        # Python 파일이나 UI 관련 파일 변경 시에만 재시작
        if event.src_path.endswith(('.py', '.txt', '.md')):
            # __pycache__ 폴더는 무시
            if '__pycache__' in event.src_path:
                return
            
            if not self.restart_pending:
                self.restart_pending = True
                print(f"\n🔄 파일 변경 감지: {os.path.basename(event.src_path)}")
                print("⏳ 1초 후 애플리케이션을 재시작합니다...")
                
                # 1초 후 재시작 (연속 변경 방지)
                def delayed_restart():
                    time.sleep(1)
                    if self.restart_pending:
                        self.restart_pending = False
                        self.start_app()
                
                import threading
                threading.Thread(target=delayed_restart, daemon=True).start()

def main():
    print("🔧 Site Creator 개발용 자동 재실행 모드")
    print("=" * 50)
    
    # 현재 디렉토리 확인
    current_dir = Path.cwd()
    app_path = current_dir / "ui.py"
    
    if not app_path.exists():
        print(f"❌ ui.py 파일을 찾을 수 없습니다: {app_path}")
        print("현재 디렉토리에서 실행해주세요.")
        return
    
    print(f"📁 모니터링 디렉토리: {current_dir}")
    print(f"🎯 대상 파일: {app_path}")
    print("\n📋 모니터링 중인 파일 확장자:")
    print("   - .py (Python 파일)")
    print("   - .txt (텍스트 파일)")
    print("   - .md (마크다운 파일)")
    print("\n💡 종료하려면 Ctrl+C를 누르세요.")
    print("=" * 50)
    
    # 이벤트 핸들러 생성
    event_handler = AppRestartHandler(app_path)
    
    # 감시자 설정
    observer = Observer()
    observer.schedule(event_handler, str(current_dir), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 개발 모드 종료 중...")
        event_handler.stop_app()
        observer.stop()
        observer.join()
        print("👋 개발 모드가 종료되었습니다.")

if __name__ == "__main__":
    main()
