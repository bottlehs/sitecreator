#!/usr/bin/env python3
"""
Site Creator - PyQt5 기반 범용 GUI
가장 안정적이고 크로스 플랫폼 호환성이 뛰어난 PyQt5 사용
"""

import sys
import platform
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QGroupBox, QGridLayout, QFileDialog, QMessageBox,
                             QStatusBar, QFrame)
from PyQt5.QtCore import Qt, QSize
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
    MODULES_LOADED = True
except ImportError as e:
    print(f"일부 모듈을 불러올 수 없습니다: {e}")
    MODULES_LOADED = False

class SiteCreatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("Site Creator - 웹사이트 자동 배포 도구")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(800, 600)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
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
        
        # 운영체제 정보
        os_info = f"운영체제: {platform.system()}"
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
            ("폴더 정리", 1, "background-color: #2196F3; color: white;"),
            ("HTML 정리", 2, "background-color: #2196F3; color: white;"),
            ("업로드", 3, "background-color: #FF9800; color: white;"),
            ("초기화", 4, "background-color: #F44336; color: white;"),
            ("서버 설정", 5, "background-color: #9C27B0; color: white;"),
            ("SSL 설정", 6, "background-color: #009688; color: white;"),
            ("블랙 업로드", 7, "background-color: #607D8B; color: white;"),
            ("블랙 링크", 8, "background-color: #607D8B; color: white;")
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
        
        # 테스트 버튼
        test_btn = QPushButton("입력 필드 테스트")
        test_btn.setStyleSheet("background-color: #FF5722; color: white;")
        test_btn.clicked.connect(self.test_inputs)
        button_layout.addWidget(test_btn, 3, 0, 1, 3)
        
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
            
        # 입력값 검증
        if not self.validate_inputs(button_number):
            return
            
        try:
            if button_number == 1:
                clean_folder(self.inputs['template'].text())
            elif button_number == 2:
                clean_html(self.inputs['template'].text())
            elif button_number == 3:
                upload(self.inputs['template'].text(), 
                      self.inputs['domain'].text(),
                      self.inputs['server_ip'].text(),
                      self.inputs['server_pw'].text())
            elif button_number == 4:
                clean(self.inputs['server_ip'].text(),
                     self.inputs['server_pw'].text())
            elif button_number == 5:
                server_control(self.inputs['domain'].text(),
                             self.inputs['server_ip'].text(),
                             self.inputs['server_pw'].text())
            elif button_number == 6:
                domain_control(self.inputs['domain'].text(),
                             self.inputs['server_ip'].text(),
                             self.inputs['server_pw'].text())
            elif button_number == 7:
                black_upload(self.inputs['black_file'].text(),
                           self.inputs['server_ip'].text(),
                           self.inputs['server_pw'].text())
            elif button_number == 8:
                black_server_control(self.inputs['domain'].text(),
                                   self.inputs['link'].text(),
                                   self.inputs['server_ip'].text(),
                                   self.inputs['server_pw'].text())
                                  
            self.statusBar().showMessage(f"작업 {button_number} 완료")
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"작업 실행 중 오류가 발생했습니다:\n{str(e)}")
            self.statusBar().showMessage("오류 발생")
            
    def validate_inputs(self, button_number):
        """입력값 검증"""
        required_fields = {
            1: ['template'],           # 폴더 정리
            2: ['template'],           # HTML 정리
            3: ['template', 'domain', 'server_ip', 'server_pw'],  # 업로드
            4: ['server_ip', 'server_pw'],                        # 서버 정리
            5: ['domain', 'server_ip', 'server_pw'],              # 서버 설정
            6: ['domain', 'server_ip', 'server_pw'],              # SSL 설정
            7: ['black_file', 'server_ip', 'server_pw'],          # 블랙 업로드
            8: ['domain', 'link', 'server_ip', 'server_pw']       # 블랙 서버 설정
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
        
    def set_default_values(self):
        """기본값 설정"""
        self.inputs['domain'].setText("example.com")
        self.inputs['server_ip'].setText("192.168.1.100")
        self.inputs['server_pw'].setText("password123")
        self.inputs['template'].setText("/path/to/template")
        self.inputs['black_file'].setText("/path/to/blacklist.txt")

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
