# 🌐 Site Creator 크로스 플랫폼 가이드

**Windows와 macOS에서 동일하게 사용 가능한 웹사이트 자동 배포 도구**

## 🖥️ 지원 운영체제

### ✅ **완전 지원**
- **Windows 10/11** (64비트)
- **macOS 10.14+** (Mojave 이상)
- **Linux** (Ubuntu 18.04+, Debian 9+)

### 🔧 **자동 감지 기능**
- 운영체제 자동 감지 및 최적 설정 적용
- 파일 경로 구분자 자동 처리 (`\` vs `/`)
- 운영체제별 기본 경로 자동 설정
- 네이티브 텍스트 에디터 자동 선택

## 📁 파일 경로 처리

### **Windows**
```
템플릿 경로: C:\Users\username\template
블랙 파일: C:\Users\username\blacklist.txt
설정 파일: server_config.txt
```

### **macOS/Linux**
```
템플릿 경로: /Users/username/template
블랙 파일: /Users/username/blacklist.txt
설정 파일: server_config.txt
```

## ⚙️ 설정 파일 (server_config.txt)

### **Windows 예시**
```ini
[server]
domain=naunyoga.shop
server_ip=38.180.190.44
server_pw=7iS86tqTkJ
template=C:\Users\username\template
black_file=C:\Users\username\blacklist.txt
link=
```

### **macOS 예시**
```ini
[server]
domain=naunyoga.shop
server_ip=38.180.190.44
server_pw=7iS86tqTkJ
template=/Users/username/template
black_file=/Users/username/blacklist.txt
link=
```

## 🚀 실행 방법

### **Windows**
```cmd
# 명령 프롬프트에서
cd site_creator
python ui.py
```

### **macOS**
```bash
# 터미널에서
cd site_creator
python3 ui.py
```

## 🔧 운영체제별 특징

### **Windows**
- **설정 파일 열기**: 메모장(notepad) 자동 실행
- **파일 경로**: 백슬래시(`\`) 사용
- **기본 경로**: `C:\Users\username\`
- **터미널**: 명령 프롬프트 또는 PowerShell

### **macOS**
- **설정 파일 열기**: 텍스트에디트 자동 실행
- **파일 경로**: 슬래시(`/`) 사용
- **기본 경로**: `/Users/username/`
- **터미널**: Terminal.app

## 🛠️ 문제 해결

### **Windows에서 문제 발생 시**
1. **Python 설치 확인**: `python --version`
2. **PyQt5 설치**: `pip install PyQt5`
3. **관리자 권한**: 명령 프롬프트를 관리자 권한으로 실행

### **macOS에서 문제 발생 시**
1. **Python 설치 확인**: `python3 --version`
2. **PyQt5 설치**: `pip3 install PyQt5`
3. **권한 문제**: `chmod +x ui.py`

### **공통 문제**
- **tkinter 충돌**: PyQt5와 tkinter 동시 사용 시 충돌 방지됨
- **파일 경로**: 운영체제별 경로 구분자 자동 처리
- **인코딩**: UTF-8로 통일하여 한글 지원

## 📋 체크리스트

### **Windows 사용자**
- [ ] Python 3.9+ 설치 확인
- [ ] PyQt5 설치 확인
- [ ] 관리자 권한으로 실행
- [ ] Windows Defender 예외 설정 (필요시)

### **macOS 사용자**
- [ ] Python 3.9+ 설치 확인
- [ ] PyQt5 설치 확인
- [ ] 터미널 권한 확인
- [ ] 보안 설정에서 Python 허용

## 🎯 최적화 팁

### **성능 향상**
- SSD 사용 권장
- 충분한 RAM (최소 4GB)
- 안정적인 인터넷 연결

### **사용성 향상**
- 설정 파일 미리 준비
- 템플릿 폴더 구조 정리
- 서버 정보 정확히 입력

## 📞 지원

### **운영체제별 지원**
- **Windows**: Windows 10/11 최적화
- **macOS**: macOS 10.14+ 최적화
- **Linux**: Ubuntu/Debian 계열 지원

### **문제 신고 시 포함할 정보**
- 운영체제 버전
- Python 버전
- 오류 메시지 전체
- 실행 환경 (터미널/IDE)

---

**Site Creator**는 Windows와 macOS에서 동일한 사용자 경험을 제공합니다! 🚀
