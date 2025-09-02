#!/usr/bin/env python3
"""
Site Creator - PyQt5 기반 범용 GUI
가장 안정적이고 크로스 플랫폼 호환성이 뛰어난 PyQt5 사용
"""

import sys
import platform
import os
import configparser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QGroupBox, QGridLayout, QFileDialog, QMessageBox,
                             QStatusBar, QFrame, QTextEdit, QSplitter)
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

# Site Creator 모듈들
try:
    from cleanFolders import clean_folder
    from cleanHtml import clean_html
    from clean import clean
    from upload import upload
    from server import server_control
    from https import domain_control
    from black_upload import black_upload
    from black_server import black_server_control
    from server_check import check_server_status, auto_cleanup_server
    MODULES_LOADED = True
except ImportError as e:
    print(f"일부 모듈을 불러올 수 없습니다: {e}")
    MODULES_LOADED = False

class LogThread(QThread):
    """로그 출력을 위한 스레드"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str, str)  # 작업명, 결과 메시지
    
    def __init__(self, func, task_name="작업", *args, **kwargs):
        super().__init__()
        self.func = func
        self.task_name = task_name
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        """스레드 실행"""
        try:
            # 기존 print 함수를 임시로 교체
            import builtins
            original_print = builtins.print
            
            def log_print(*args, **kwargs):
                message = ' '.join(str(arg) for arg in args)
                self.log_signal.emit(message)
                original_print(*args, **kwargs)
            
            builtins.print = log_print
            
            # 함수 실행
            result = self.func(*self.args, **self.kwargs)
            
            # 원래 print 함수 복원
            builtins.print = original_print
            
            self.log_signal.emit("✅ 작업 완료")
            self.finished_signal.emit(self.task_name, "성공적으로 완료되었습니다!")
            
        except Exception as e:
            self.log_signal.emit(f"❌ 오류 발생: {str(e)}")
            self.finished_signal.emit(self.task_name, f"오류가 발생했습니다: {str(e)}")

class SiteCreatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_file = "server_config.txt"
        self.buttons = []  # 버튼들을 저장할 리스트 초기화
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("Site Creator - 웹사이트 자동 배포 도구")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 스플리터로 메인 영역과 로그 영역 분할
        splitter = QSplitter(Qt.Vertical)
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(splitter)
        
        # 상단: 기존 UI 영역
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        
        # 하단: 로그 영역
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        
        # 로그 제목
        log_title = QLabel("📋 실행 로그")
        log_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; margin: 5px;")
        log_layout.addWidget(log_title)
        
        # 로그 텍스트 에디터
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                border: 1px solid #34495e;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        # 로그 지우기 버튼
        self.clear_log_btn = QPushButton("🗑️ 로그 지우기")
        self.clear_log_btn.clicked.connect(self.clear_log)
        self.clear_log_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        log_layout.addWidget(self.clear_log_btn)
        
        # 스플리터에 위젯 추가
        splitter.addWidget(top_widget)
        splitter.addWidget(log_widget)
        splitter.setSizes([600, 200])  # 상단 600px, 하단 200px
        
        # 메인 레이아웃 (기존 UI)
        main_layout = top_layout
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 제목
        title_label = QLabel("Site Creator")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 운영체제 정보 (크로스 플랫폼)
        os_name = platform.system()
        os_version = platform.release()
        if os_name == "Darwin":
            os_display = "macOS"
        elif os_name == "Windows":
            os_display = "Windows"
        else:
            os_display = os_name
            
        os_info = f"운영체제: {os_display} {os_version}"
        os_label = QLabel(os_info)
        os_label.setAlignment(Qt.AlignCenter)
        os_label.setStyleSheet("color: gray; font-size: 10px;")
        main_layout.addWidget(os_label)
        
        # 입력 섹션
        self.create_input_section(main_layout)
        
        # 버튼 섹션
        self.create_button_section(main_layout)
        
        # 상태바
        self.statusBar().showMessage("준비됨")
        
        # 입력 필드에 기본값 설정
        self.set_default_values()
        
        # 로그 초기화
        self.log_thread = None
        self.is_working = False  # 작업 진행 상태 플래그
        self.add_log("🚀 Site Creator 시작됨")
        
    def create_input_section(self, parent_layout):
        """입력 섹션 생성"""
        input_group = QGroupBox("설정 정보")
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(10)
        
        # 입력 필드들
        self.inputs = {}
        
        # 도메인
        domain_layout = QHBoxLayout()
        domain_label = QLabel("도메인:")
        domain_label.setFixedWidth(80)
        self.inputs['domain'] = QLineEdit()
        self.inputs['domain'].setPlaceholderText("example.com")
        domain_layout.addWidget(domain_label)
        domain_layout.addWidget(self.inputs['domain'])
        input_layout.addLayout(domain_layout)
        
        # 링크
        link_layout = QHBoxLayout()
        link_label = QLabel("링크:")
        link_label.setFixedWidth(80)
        self.inputs['link'] = QLineEdit()
        self.inputs['link'].setPlaceholderText("https://example.com")
        link_layout.addWidget(link_label)
        link_layout.addWidget(self.inputs['link'])
        input_layout.addLayout(link_layout)
        
        # 서버 IP
        ip_layout = QHBoxLayout()
        ip_label = QLabel("서버 IP:")
        ip_label.setFixedWidth(80)
        self.inputs['server_ip'] = QLineEdit()
        self.inputs['server_ip'].setPlaceholderText("192.168.1.100")
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.inputs['server_ip'])
        input_layout.addLayout(ip_layout)
        
        # 서버 비밀번호
        pw_layout = QHBoxLayout()
        pw_label = QLabel("서버 PW:")
        pw_label.setFixedWidth(80)
        self.inputs['server_pw'] = QLineEdit()
        self.inputs['server_pw'].setEchoMode(QLineEdit.Password)
        self.inputs['server_pw'].setPlaceholderText("비밀번호 입력")
        pw_layout.addWidget(pw_label)
        pw_layout.addWidget(self.inputs['server_pw'])
        input_layout.addLayout(pw_layout)
        
        # 템플릿
        template_layout = QHBoxLayout()
        template_label = QLabel("Template:")
        template_label.setFixedWidth(80)
        self.inputs['template'] = QLineEdit()
        self.inputs['template'].setPlaceholderText("템플릿 폴더 경로")
        template_browse = QPushButton("Browse")
        template_browse.clicked.connect(lambda: self.browse_directory(self.inputs['template']))
        template_layout.addWidget(template_label)
        template_layout.addWidget(self.inputs['template'])
        template_layout.addWidget(template_browse)
        input_layout.addLayout(template_layout)
        
        # 블랙 파일
        black_layout = QHBoxLayout()
        black_label = QLabel("블랙 파일:")
        black_label.setFixedWidth(80)
        self.inputs['black_file'] = QLineEdit()
        self.inputs['black_file'].setPlaceholderText("블랙리스트 파일 경로")
        black_browse = QPushButton("Browse")
        black_browse.clicked.connect(lambda: self.browse_file(self.inputs['black_file']))
        black_layout.addWidget(black_label)
        black_layout.addWidget(self.inputs['black_file'])
        black_layout.addWidget(black_browse)
        input_layout.addLayout(black_layout)
        
        parent_layout.addWidget(input_group)
        
    def create_button_section(self, parent_layout):
        """버튼 섹션 생성"""
        button_group = QGroupBox("작업 실행")
        button_layout = QGridLayout(button_group)
        button_layout.setSpacing(10)
        
        # 버튼 데이터
        buttons_data = [
            ("🚀 원스톱 실행", 0, "background-color: #E91E63; color: white; font-weight: bold; font-size: 14px;"),
            ("서버 점검", 1, "background-color: #4CAF50; color: white; font-weight: bold;"),
            ("폴더 정리", 2, "background-color: #2196F3; color: white;"),
            ("HTML 정리", 3, "background-color: #2196F3; color: white;"),
            ("업로드", 4, "background-color: #FF9800; color: white;"),
            ("초기화", 5, "background-color: #F44336; color: white;"),
            ("서버 설정", 6, "background-color: #9C27B0; color: white;"),
            ("SSL 설정", 7, "background-color: #009688; color: white;"),
            ("블랙 업로드", 8, "background-color: #607D8B; color: white;"),
            ("블랙 링크", 9, "background-color: #607D8B; color: white;")
        ]
        
        # 버튼 생성
        for i, (text, num, style) in enumerate(buttons_data):
            row = i // 3
            col = i % 3
            btn = QPushButton(text)
            btn.setStyleSheet(style)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, n=num: self.on_button_click(n))
            button_layout.addWidget(btn, row, col)
            self.buttons.append(btn)  # 버튼을 리스트에 저장
        
        # 테스트 버튼
        test_btn = QPushButton("입력 필드 테스트")
        test_btn.setStyleSheet("background-color: #FF5722; color: white;")
        test_btn.clicked.connect(self.test_inputs)
        button_layout.addWidget(test_btn, 3, 0, 1, 1)
        
        # 설정 파일 다시 읽기 버튼
        reload_btn = QPushButton("설정 파일 다시 읽기")
        reload_btn.setStyleSheet("background-color: #795548; color: white;")
        reload_btn.clicked.connect(self.reload_config)
        button_layout.addWidget(reload_btn, 3, 1, 1, 1)
        
        # 설정 파일 열기 버튼
        open_config_btn = QPushButton("설정 파일 열기")
        open_config_btn.setStyleSheet("background-color: #607D8B; color: white;")
        open_config_btn.clicked.connect(self.open_config_file)
        button_layout.addWidget(open_config_btn, 3, 2, 1, 1)
        
        parent_layout.addWidget(button_group)
        
    def browse_directory(self, line_edit):
        """폴더 선택"""
        folder = QFileDialog.getExistingDirectory(self, "폴더 선택")
        if folder:
            line_edit.setText(folder)
            
    def browse_file(self, line_edit):
        """파일 선택"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "파일 선택", "", 
            "모든 파일 (*);;HTML 파일 (*.html);;텍스트 파일 (*.txt)"
        )
        if file_path:
            line_edit.setText(file_path)
            
    def on_button_click(self, button_number):
        """버튼 클릭 이벤트"""
        if not MODULES_LOADED:
            QMessageBox.warning(self, "경고", "일부 모듈이 로드되지 않았습니다.")
            return
        
        # 작업 중인지 확인
        if self.is_working:
            QMessageBox.warning(self, "작업 진행 중", "현재 작업이 진행 중입니다. 완료 후 다시 시도해주세요.")
            return
            
        # 입력값 검증
        if not self.validate_inputs(button_number):
            return
            
        try:
            if button_number == 0:
                # 원스톱 실행
                self.full_automation()
            elif button_number == 1:
                # 서버 점검
                self.check_server()
            elif button_number == 2:
                # 폴더 정리
                self.add_log("📁 폴더 정리 시작...")
                self.run_with_log(clean_folder, "폴더 정리", self.inputs['template'].text())
            elif button_number == 3:
                # HTML 정리
                self.add_log("🔧 HTML 정리 시작...")
                self.run_with_log(clean_html, "HTML 정리", self.inputs['template'].text())
            elif button_number == 4:
                # 업로드
                self.add_log("📤 파일 업로드 시작...")
                self.run_with_log(upload, "업로드", 
                                self.inputs['template'].text(), 
                                self.inputs['domain'].text(),
                                self.inputs['server_ip'].text(),
                                self.inputs['server_pw'].text())
            elif button_number == 5:
                # 서버 정리
                self.add_log("🧹 서버 정리 시작...")
                self.run_with_log(clean, "서버 정리",
                                self.inputs['server_ip'].text(),
                                self.inputs['server_pw'].text())
            elif button_number == 6:
                # 서버 설정 전 자동 점검
                self.server_control_with_check()
            elif button_number == 7:
                # SSL 설정
                self.add_log("🔒 SSL 설정 시작...")
                self.run_with_log(domain_control, "SSL 설정",
                                self.inputs['domain'].text(),
                                self.inputs['server_ip'].text(),
                                self.inputs['server_pw'].text())
            elif button_number == 8:
                # 블랙 업로드
                self.add_log("📤 블랙 파일 업로드 시작...")
                self.run_with_log(black_upload, "블랙 업로드",
                                self.inputs['black_file'].text(),
                                self.inputs['server_ip'].text(),
                                self.inputs['server_pw'].text())
            elif button_number == 9:
                # 블랙 서버 설정
                self.add_log("⚙️ 블랙 서버 설정 시작...")
                self.run_with_log(black_server_control, "블랙 서버 설정",
                                self.inputs['domain'].text(),
                                self.inputs['link'].text(),
                                self.inputs['server_ip'].text(),
                                self.inputs['server_pw'].text())
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"작업 실행 중 오류가 발생했습니다:\n{str(e)}")
            self.statusBar().showMessage("오류 발생")
            
    def validate_inputs(self, button_number):
        """입력값 검증"""
        required_fields = {
            0: ['template', 'domain', 'server_ip', 'server_pw'],  # 원스톱 실행
            1: ['server_ip', 'server_pw'],                        # 서버 점검
            2: ['template'],           # 폴더 정리
            3: ['template'],           # HTML 정리
            4: ['template', 'domain', 'server_ip', 'server_pw'],  # 업로드
            5: ['server_ip', 'server_pw'],                        # 서버 정리
            6: ['domain', 'server_ip', 'server_pw'],              # 서버 설정
            7: ['domain', 'server_ip', 'server_pw'],              # SSL 설정
            8: ['black_file', 'server_ip', 'server_pw'],          # 블랙 업로드
            9: ['domain', 'link', 'server_ip', 'server_pw']       # 블랙 서버 설정
        }
        
        if button_number not in required_fields:
            return True
            
        for field in required_fields[button_number]:
            if not self.inputs[field].text().strip():
                QMessageBox.warning(self, "입력 오류", f"'{field}' 필드를 입력해주세요.")
                self.inputs[field].setFocus()
                return False
                
        return True
            
    def test_inputs(self):
        """입력 필드 테스트"""
        print("\n=== 입력 필드 테스트 ===")
        for name, widget in self.inputs.items():
            test_value = f"테스트 {name}"
            widget.setText(test_value)
            print(f"{name}: {widget.text()}")
            print(f"위치: ({widget.x()}, {widget.y()})")
            print(f"크기: {widget.width()}x{widget.height()}")
            print(f"보임 여부: {widget.isVisible()}")
            print("---")
            
        QMessageBox.information(self, "테스트 완료", "모든 입력 필드에 테스트 값을 설정했습니다.")
        
    def check_server(self):
        """서버 점검 실행"""
        self.add_log("🔍 서버 점검 시작...")
        self.run_with_log(check_server_status, "서버 점검",
                         self.inputs['server_ip'].text(),
                         self.inputs['server_pw'].text())
    
    def server_control_with_check(self):
        """서버 설정 전 자동 점검 후 설정"""
        self.add_log("🚀 서버 설정 시작 (자동 점검 포함)...")
        
        def run_server_setup():
            # 1단계: 서버 점검
            self.add_log("1️⃣ 서버 점검 중...")
            success, message = check_server_status(
                self.inputs['server_ip'].text(),
                self.inputs['server_pw'].text()
            )
            
            if not success:
                self.add_log(f"❌ 서버 점검 실패: {message}")
                return
            
            if "경고사항이 있습니다" in message:
                self.add_log(f"⚠️ 경고사항 발견: {message}")
            
            # 2단계: 자동 정리
            self.add_log("2️⃣ 서버 정리 중...")
            cleanup_success, cleanup_message = auto_cleanup_server(
                self.inputs['server_ip'].text(),
                self.inputs['server_pw'].text()
            )
            
            if not cleanup_success:
                self.add_log(f"⚠️ 서버 정리 경고: {cleanup_message}")
            
            # 3단계: 서버 설정
            self.add_log("3️⃣ 서버 설정 중...")
            server_control(
                self.inputs['domain'].text(),
                self.inputs['server_ip'].text(),
                self.inputs['server_pw'].text()
            )
            
            # 4단계: 검증
            self.add_log("4️⃣ 서버 검증 중...")
            success, message = check_server_status(
                self.inputs['server_ip'].text(),
                self.inputs['server_pw'].text()
            )
            
            if success:
                self.add_log("✅ 서버 설정 완료!")
            else:
                self.add_log(f"⚠️ 서버 설정 완료 (검증 경고: {message})")
        
        self.run_with_log(run_server_setup, "서버 설정")
    
    def full_automation(self):
        """원스톱 실행: 서버 정보만 입력하면 모든 과정을 자동으로 처리"""
        self.add_log("🚀 원스톱 실행 시작...")
        
        def run_full_automation():
            try:
                # 1단계: 서버 점검
                self.add_log("1️⃣ 서버 점검 중...")
                success, message = check_server_status(
                    self.inputs['server_ip'].text(),
                    self.inputs['server_pw'].text()
                )
                
                if not success:
                    self.add_log(f"❌ 서버 점검 실패: {message}")
                    return
                
                if "경고사항이 있습니다" in message:
                    self.add_log(f"⚠️ 경고사항 발견: {message}")
                
                # 2단계: 폴더 정리
                self.add_log("2️⃣ 폴더 정리 중...")
                clean_folder(self.inputs['template'].text())
                
                # 3단계: HTML 정리
                self.add_log("3️⃣ HTML 정리 중...")
                clean_html(self.inputs['template'].text())
                
                # 4단계: 업로드
                self.add_log("4️⃣ 파일 업로드 중...")
                upload(
                    self.inputs['template'].text(), 
                    self.inputs['domain'].text(),
                    self.inputs['server_ip'].text(),
                    self.inputs['server_pw'].text()
                )
                
                # 5단계: 서버 정리
                self.add_log("5️⃣ 서버 정리 중...")
                auto_cleanup_server(
                    self.inputs['server_ip'].text(),
                    self.inputs['server_pw'].text()
                )
                
                # 6단계: 서버 설정
                self.add_log("6️⃣ 서버 설정 중...")
                server_control(
                    self.inputs['domain'].text(),
                    self.inputs['server_ip'].text(),
                    self.inputs['server_pw'].text()
                )
                
                # 7단계: SSL 설정
                self.add_log("7️⃣ SSL 설정 중...")
                domain_control(
                    self.inputs['domain'].text(),
                    self.inputs['server_ip'].text(),
                    self.inputs['server_pw'].text()
                )
                
                # 8단계: 최종 검증
                self.add_log("8️⃣ 최종 검증 중...")
                success, message = check_server_status(
                    self.inputs['server_ip'].text(),
                    self.inputs['server_pw'].text()
                )
                
                if success:
                    self.add_log("🎉 원스톱 실행 성공!")
                    self.add_log(f"🌐 웹사이트: https://{self.inputs['domain'].text()}")
                else:
                    self.add_log(f"⚠️ 원스톱 실행 완료 (검증 경고: {message})")
                
            except Exception as e:
                self.add_log(f"❌ 자동화 중 오류: {str(e)}")
                raise e
        
        self.run_with_log(run_full_automation, "원스톱 실행")

    def load_config_file(self):
        """설정 파일에서 값 읽어오기 (크로스 플랫폼)"""
        # 운영체제별 기본 경로 설정
        if platform.system() == "Windows":
            default_template = "C:\\Users\\username\\template"
            default_black_file = "C:\\Users\\username\\blacklist.txt"
        else:  # macOS, Linux
            default_template = "/path/to/template"
            default_black_file = "/path/to/blacklist.txt"
            
        config_values = {
            'domain': 'example.com',
            'server_ip': '192.168.1.100',
            'server_pw': 'password123',
            'template': default_template,
            'black_file': default_black_file,
            'link': ''
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                # 빈 파일이 아닌 경우에만 파싱
                if content:
                    config = configparser.ConfigParser()
                    config.read(self.config_file, encoding='utf-8')
                    
                    # 설정 파일에서 값 읽어오기
                    if 'server' in config:
                        for key in config_values.keys():
                            if key in config['server']:
                                value = config['server'][key].strip()
                                if value:  # 빈 값이 아닌 경우에만 설정
                                    config_values[key] = value
                    
                    print(f"설정 파일에서 값 로드됨: {config_values}")
                else:
                    print("설정 파일이 비어있음 - 기본값 사용")
            else:
                print("설정 파일이 없음 - 기본값 사용")
                
        except Exception as e:
            print(f"설정 파일 읽기 오류: {e} - 기본값 사용")
            
        return config_values

    def set_default_values(self):
        """기본값 설정"""
        config_values = self.load_config_file()
        
        self.inputs['domain'].setText(config_values['domain'])
        self.inputs['server_ip'].setText(config_values['server_ip'])
        self.inputs['server_pw'].setText(config_values['server_pw'])
        self.inputs['template'].setText(config_values['template'])
        self.inputs['black_file'].setText(config_values['black_file'])
        self.inputs['link'].setText(config_values['link'])
    
    def reload_config(self):
        """설정 파일 다시 읽기"""
        try:
            self.set_default_values()
            QMessageBox.information(self, "설정 파일 다시 읽기", "설정 파일에서 값을 다시 읽어왔습니다.")
            self.statusBar().showMessage("설정 파일 다시 읽기 완료")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"설정 파일 읽기 중 오류가 발생했습니다:\n{str(e)}")
    
    def open_config_file(self):
        """설정 파일 열기 (크로스 플랫폼)"""
        try:
            if os.path.exists(self.config_file):
                system = platform.system()
                
                if system == "Darwin":  # macOS
                    os.system(f"open -e '{self.config_file}'")
                elif system == "Windows":  # Windows
                    os.system(f'notepad "{self.config_file}"')
                else:  # Linux 및 기타
                    os.system(f"xdg-open '{self.config_file}'")
                
                QMessageBox.information(self, "설정 파일 열기", 
                    f"설정 파일을 열었습니다.\n\n파일을 수정한 후 '설정 파일 다시 읽기' 버튼을 클릭하세요.")
            else:
                QMessageBox.warning(self, "파일 없음", 
                    f"설정 파일 '{self.config_file}'이 존재하지 않습니다.\n\n기본값이 사용됩니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"설정 파일 열기 중 오류가 발생했습니다:\n{str(e)}")
    
    def add_log(self, message):
        """로그 메시지 추가"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        self.log_text.append(log_message)
        
        # 자동 스크롤
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # 상태바에도 표시
        self.statusBar().showMessage(message, 3000)
    
    def clear_log(self):
        """로그 지우기"""
        self.log_text.clear()
        self.add_log("📋 로그가 지워졌습니다")
    
    def run_with_log(self, func, task_name="작업", *args, **kwargs):
        """로그와 함께 함수 실행"""
        if self.log_thread and self.log_thread.isRunning():
            QMessageBox.warning(self, "경고", "이미 작업이 실행 중입니다. 잠시 기다려주세요.")
            return
        
        # 작업 시작 시 버튼 비활성화
        self.set_buttons_enabled(False)
        
        self.log_thread = LogThread(func, task_name, *args, **kwargs)
        self.log_thread.log_signal.connect(self.add_log)
        self.log_thread.finished_signal.connect(self.on_task_finished)
        self.log_thread.finished.connect(lambda: self.set_buttons_enabled(True))  # 작업 완료 시 버튼 활성화
        self.log_thread.start()
    
    def on_task_finished(self, task_name, result_message):
        """작업 완료 시 호출"""
        # 작업별 구체적인 안내창 표시
        if "서버 점검" in task_name:
            if "성공적으로 완료" in result_message:
                QMessageBox.information(self, "🔍 서버 점검 완료", 
                    f"서버 점검이 완료되었습니다!\n\n{result_message}\n\n하단 로그에서 상세 결과를 확인하세요.")
            else:
                QMessageBox.warning(self, "🔍 서버 점검 실패", 
                    f"서버 점검 중 문제가 발생했습니다:\n\n{result_message}\n\n하단 로그를 확인하세요.")
        
        elif "서버 설정" in task_name:
            if "성공적으로 완료" in result_message:
                QMessageBox.information(self, "⚙️ 서버 설정 완료", 
                    f"서버 설정이 완료되었습니다!\n\n{result_message}\n\n웹사이트가 정상적으로 배포되었습니다.")
            else:
                QMessageBox.critical(self, "⚙️ 서버 설정 실패", 
                    f"서버 설정 중 오류가 발생했습니다:\n\n{result_message}\n\n하단 로그를 확인하세요.")
        
        elif "폴더 정리" in task_name:
            QMessageBox.information(self, "📁 폴더 정리 완료", 
                f"폴더 정리가 완료되었습니다!\n\n{result_message}")
        
        elif "HTML 정리" in task_name:
            QMessageBox.information(self, "🔧 HTML 정리 완료", 
                f"HTML 정리가 완료되었습니다!\n\n{result_message}")
        
        elif "업로드" in task_name:
            QMessageBox.information(self, "📤 업로드 완료", 
                f"파일 업로드가 완료되었습니다!\n\n{result_message}")
        
        elif "SSL 설정" in task_name:
            QMessageBox.information(self, "🔒 SSL 설정 완료", 
                f"SSL 인증서 설정이 완료되었습니다!\n\n{result_message}")
        
        else:
            # 기본 안내창
            QMessageBox.information(self, f"✅ {task_name} 완료", 
                f"{task_name}이 완료되었습니다!\n\n{result_message}")
        
        self.statusBar().showMessage(f"{task_name} 완료", 5000)
    
    def set_buttons_enabled(self, enabled):
        """작업 버튼들 활성화/비활성화 (로그 지우기 버튼 제외)"""
        for btn in self.buttons:
            btn.setEnabled(enabled)
            # 비활성화 시 시각적 피드백
            if not enabled:
                btn.setStyleSheet(btn.styleSheet() + """
                    QPushButton:disabled {
                        background-color: #cccccc;
                        color: #666666;
                        border: 1px solid #999999;
                    }
                """)
        
        # 로그 지우기 버튼은 항상 활성화
        if hasattr(self, 'clear_log_btn'):
            self.clear_log_btn.setEnabled(True)
        
        # 작업 상태에 따른 스타일 변경
        if enabled:
            self.is_working = False
            self.statusBar().showMessage("준비됨")
        else:
            self.is_working = True
            self.statusBar().showMessage("작업 진행 중...")

def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    
    # 애플리케이션 스타일 설정
    app.setStyle('Fusion')
    
    # 윈도우 생성 및 표시
    window = SiteCreatorGUI()
    window.show()
    
    print("PyQt5 기반 Site Creator GUI 시작됨")
    print("입력 필드가 제대로 보이는지 확인해주세요.")
    
    # 이벤트 루프 시작
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
