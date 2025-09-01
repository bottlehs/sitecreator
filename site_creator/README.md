# 🚀 Site Creator

**웹사이트 자동 배포 및 관리 도구**

Site Creator는 Flask 기반 웹 애플리케이션을 원격 서버에 자동으로 설정하고 배포하는 Python 도구입니다. nginx 설정, SSL 인증서 설정, 트래픽 제어 등을 자동화하여 웹사이트 배포 프로세스를 간소화합니다.

## ✨ 주요 기능

- 🔧 **자동 서버 설정**: nginx, Flask, SSL 인증서 자동 구성
- 📤 **원클릭 배포**: 로컬 템플릿을 원격 서버에 자동 업로드
- 🎯 **트래픽 제어**: 화이트/블랙 모드로 광고 트래픽 분기
- 🧹 **파일 최적화**: HTML 정리, 폴더 구조 최적화
- 🔒 **보안 설정**: 방화벽 설정, 권한 관리 자동화
- 📱 **봇 차단**: User-Agent 분석을 통한 봇 트래픽 필터링

## 🏗️ 프로젝트 구조

```
site_creator/
├── ui.py                 # PyQt5 기반 메인 GUI 인터페이스
├── server.py            # 서버 설정 및 초기화
├── upload.py            # 파일 업로드 관리
├── https.py             # SSL 인증서 설정
├── black_server.py      # 블랙리스트 서버 제어
├── clean.py             # 서버 정리 및 초기화
├── cleanFolders.py      # 로컬 폴더 정리 및 압축
├── cleanHtml.py         # HTML 파일 정리 및 최적화
├── page_default/        # Flask 애플리케이션 템플릿
│   ├── flaskapp.py     # 메인 Flask 애플리케이션
│   ├── handlers/       # 페이지 라우팅 및 로직
│   ├── templates/      # HTML 템플릿
│   └── requirements.txt # Flask 앱 의존성
├── requirements.txt     # 메인 프로젝트 의존성
├── setup.sh            # macOS/Linux 설치 스크립트
├── setup.bat           # Windows 설치 스크립트
├── dev.sh              # macOS/Linux 개발 모드 스크립트
├── dev.bat             # Windows 개발 모드 배치 파일
├── dev_run.py          # 자동 재실행 핵심 스크립트
├── build_windows_only.py # Windows EXE 빌드 스크립트
└── README.md           # 프로젝트 문서
```

## 🚀 빠른 시작

### 시스템 요구사항

- **Python**: **3.13 이상 (권장)**, 3.9+ (최소)
- **OS**: Windows, macOS, Linux
- **서버**: Ubuntu/Debian 기반 (root 계정 필요)

> 💡 **Python 3.13 권장 이유**: 최신 기능과 보안 업데이트, 향상된 성능, 최신 패키지 호환성

### 1. 프로젝트 클론

```bash
git clone <repository-url>
cd site_creator
```

### 2. 자동 설치 (권장)

#### Python 3.13 환경 설정 (새로 추가)
```bash
# macOS/Linux
./setup_python313.sh

# Windows
setup_python313.bat
```

#### 기존 설치 방법
```bash
# macOS/Linux
./setup.sh

# Windows
setup.bat
```

### 3. 수동 설치

#### Python 3.13 환경 (권장)
```bash
# 가상환경 생성
python3.13 -m venv venv

# 가상환경 활성화
source venv/bin/activate          # macOS/Linux
# 또는
venv\Scripts\activate.bat         # Windows

# 의존성 설치
pip install -r requirements.txt
```

#### 기존 Python 버전
```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate          # macOS/Linux
# 또는
venv\Scripts\activate.bat         # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 4. 애플리케이션 실행

#### PyQt5 기반 GUI 실행 (권장)
```bash
# 가상환경 활성화 후
python ui.py
```

#### Windows EXE 파일 생성
```cmd
# Windows에서만 실행 가능
python build_windows_only.py

# 또는 배치 파일 사용
build_exe.bat
```

### 5. Python 3.13 호환성 확인

프로젝트가 Python 3.13에서 정상 작동하는지 확인하려면:

```bash
# 호환성 검사 실행
python check_python_version.py

# 또는 가상환경 활성화 후
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate.bat         # Windows
python check_python_version.py
```

이 스크립트는 다음을 확인합니다:
- ✅ Python 3.13+ 버전 확인
- ✅ 필수 패키지 설치 상태
- ✅ PyInstaller 6.0.0+ 호환성
- 🔧 Python 3.13 가상환경 생성 가이드

**생성된 파일**: `dist/SiteCreator.exe`
**특징**: 
- Python 설치 없이 실행 가능
- 단일 exe 파일로 모든 의존성 포함
- Windows에서 더블클릭으로 실행

#### macOS DMG 파일 생성
```bash
# macOS에서만 실행 가능
python build_macos.py

# 또는 쉘 스크립트 사용
./build_macos.sh
```

**생성된 파일들**:
- `dist/SiteCreator/`: 실행 파일 및 의존성
- `dist/SiteCreator.app`: 앱 번들
- `SiteCreator_macOS.dmg`: 설치용 DMG 파일

**특징**:
- Intel + Apple Silicon 모두 지원
- macOS 네이티브 앱 번들
- DMG 파일로 쉬운 설치

#### 개발 모드 (자동 재실행)
```bash
# macOS/Linux
./dev.sh

# Windows
dev.bat
```

**PyQt5 GUI 특징:**
- 크로스 플랫폼 호환성 (Mac, Windows, Linux)
- 안정적이고 현대적인 사용자 인터페이스
- 모든 입력 필드가 완벽하게 표시
- 네이티브 운영체제 느낌

**개발 모드 특징:**
- 파일 변경 시 자동으로 애플리케이션 재시작
- Python, 텍스트, 마크다운 파일 변경 감지
- 연속 변경 방지 (1초 지연)
- 개발 중 편리한 자동 재시작

## 📋 사용 방법

### GUI 인터페이스

1. **도메인**: 배포할 웹사이트 도메인 입력
2. **링크**: 블랙리스트 링크 (선택사항)
3. **서버 IP**: 원격 서버 IP 주소
4. **서버 PW**: 원격 서버 root 비밀번호
5. **Template**: 로컬 템플릿 폴더 경로 선택
6. **블랙 파일**: 블랙리스트 파일 경로 (선택사항)

### 작업 순서

1. **폴더 정리**: 템플릿 폴더 정리 및 압축
2. **HTML 정리**: HTML 파일 최적화
3. **업로드**: 서버에 파일 업로드
4. **서버 설정**: nginx 및 Flask 설정
5. **SSL 설정**: Let's Encrypt 인증서 설정

## 🔧 주요 모듈 설명

### `ui.py`
- PyQt5 기반 현대적 GUI 인터페이스
- 크로스 플랫폼 호환성 및 안정성
- 사용자 입력 처리 및 버튼 이벤트 관리

### `server.py`
- SSH를 통한 원격 서버 설정
- nginx 설정 파일 자동 생성
- Flask 애플리케이션 자동 배포

### `upload.py`
- SFTP를 통한 파일 업로드
- 폴더 구조 유지하며 재귀적 업로드
- 업로드 상태 모니터링

### `https.py`
- Let's Encrypt 인증서 자동 설정
- certbot을 통한 SSL 설정

### `black_server.py`
- 블랙리스트 기반 트래픽 제어
- 광고 캠페인 ID 기반 라우팅

### `clean*.py`
- 파일 및 폴더 정리
- HTML 최적화 및 템플릿 변수 처리

## 🌐 웹 애플리케이션

### Flask 앱 구조
- **라우팅**: 메인 페이지 및 동적 라우팅
- **템플릿**: 화이트/블랙 페이지 분기
- **미들웨어**: User-Agent 분석 및 봇 차단

### 트래픽 제어
- **화이트 모드**: 일반 사용자에게 메인 페이지 제공
- **블랙 모드**: 특정 광고 캠페인 트래픽을 블랙 페이지로 라우팅

## ⚠️ 주의사항

### 보안
- **root 계정**: 서버 설정 시 root 권한 필요
- **방화벽**: UFW 설정으로 포트 제어
- **SSL**: Let's Encrypt 인증서 자동 갱신

### 서버 요구사항
- **OS**: Ubuntu 18.04+ 또는 Debian 9+
- **권한**: root 계정 SSH 접근 가능
- **방화벽**: UFW 설정 가능

### 백업
- 배포 전 기존 데이터 백업 권장
- 설정 파일 변경 시 백업 필수

## 🐛 문제 해결

### 일반적인 문제

#### SSH 연결 오류
```bash
# 방화벽 설정 확인
sudo ufw status

# SSH 포트 확인
sudo netstat -tlnp | grep :22
```

#### SSL 인증서 오류
```bash
# 도메인 DNS 설정 확인
nslookup yourdomain.com

# certbot 상태 확인
sudo certbot certificates
```

#### Flask 서비스 오류
```bash
# 서비스 상태 확인
sudo systemctl status flask

# 로그 확인
sudo journalctl -u flask -f
```

## 📚 의존성

### 필수 패키지
- **paramiko**: SSH 연결 및 파일 전송
- **Flask**: 웹 애플리케이션 프레임워크
- **beautifulsoup4**: HTML 파싱 및 정리
- **user-agents**: 사용자 에이전트 파싱
- **gunicorn**: WSGI 서버
- **PyQt5**: 크로스 플랫폼 GUI 프레임워크

### 선택 패키지
- **requests**: HTTP 요청 처리
- **lxml**: XML/HTML 파서

## 🌐 크로스 플랫폼 지원

### 지원 운영체제
- **macOS**: 10.14+ (Mojave 이상)
- **Windows**: 10+ (64비트)
- **Linux**: Ubuntu 18.04+, Debian 9+, CentOS 7+

### 운영체제별 최적화
- **macOS**: PyQt5 네이티브 위젯, macOS 디자인 가이드라인 준수
- **Windows**: PyQt5 네이티브 위젯, Windows 디자인 가이드라인 준수
- **Linux**: PyQt5 네이티브 위젯, GTK 테마 호환

### 자동 감지 기능
- 운영체제 자동 감지 및 최적 설정 적용
- 화면 해상도에 따른 윈도우 크기 자동 조정
- 다크 모드 지원 (macOS, Windows)
- 운영체제별 파일 경로 구분자 자동 처리

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원

문제가 발생하거나 질문이 있으시면:
- [Issues](../../issues) 페이지에 문제를 등록해주세요
- 프로젝트 문서를 참조해주세요

## 🔄 업데이트 내역

### v1.1.0
- PyQt5 기반 GUI로 업그레이드
- 크로스 플랫폼 호환성 대폭 향상
- 입력 필드 가시성 문제 완전 해결
- 현대적이고 안정적인 사용자 인터페이스

### v1.0.0
- 초기 릴리스
- 기본 웹사이트 배포 기능
- SSL 인증서 자동 설정
- 트래픽 제어 시스템

---

**Site Creator**로 웹사이트 배포를 간단하고 효율적으로 만들어보세요! 🚀
