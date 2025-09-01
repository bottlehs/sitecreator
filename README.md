# 🚀 Site Creator

**웹사이트 자동 배포 및 관리 도구**

Site Creator는 Flask 기반 웹 애플리케이션을 원격 서버에 자동으로 설정하고 배포하는 Python 도구입니다.

## 📁 프로젝트 구조

```
sitecreator.git/
├── site_creator/          # 메인 프로젝트 디렉토리
│   ├── ui.py                 # PyQt5 기반 GUI 인터페이스
│   ├── server.py             # 서버 설정 관리
│   ├── upload.py             # 파일 업로드
│   ├── https.py              # SSL 설정
│   ├── black_server.py       # 블랙리스트 제어
│   ├── clean*.py             # 파일 정리 도구
│   ├── page_default/         # Flask 앱 템플릿
│   ├── requirements.txt      # 의존성 목록
│   ├── setup.sh              # 설치 스크립트 (macOS/Linux)
│   ├── setup.bat             # 설치 스크립트 (Windows)
│   ├── build_macos.py        # macOS DMG 빌드 스크립트
│   ├── build_windows_only.py # Windows EXE 빌드 스크립트
│   ├── dev_run.py            # 개발 모드 자동 재실행
│   ├── USER_MANUAL.md        # 상세 사용자 메뉴얼
│   ├── QUICK_START.md        # 빠른 시작 가이드
│   └── README.md             # 상세 문서
└── README.md             # 이 파일
```

## 🚀 빠른 시작

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd sitecreator.git/site_creator
```

### 2. 자동 설치
```bash
# macOS/Linux
./setup.sh

# Windows
setup.bat
```

### 3. 실행
```bash
source venv/bin/activate && python ui.py
```

## 📖 자세한 문서

프로젝트의 상세한 사용법과 설정 방법은 다음 문서들을 참조하세요:

- **📖 상세 사용법**: [`USER_MANUAL.md`](site_creator/USER_MANUAL.md) - 완전한 사용자 메뉴얼
- **⚡ 빠른 시작**: [`QUICK_START.md`](site_creator/QUICK_START.md) - 5분 퀵 스타트 가이드
- **📋 프로젝트 상태**: [`PROJECT_STATUS.md`](site_creator/PROJECT_STATUS.md) - 개발 진행 상황

## ✨ 주요 기능

- 🔧 **자동 서버 설정**: nginx, Flask, SSL 자동 구성
- 📤 **원클릭 배포**: 로컬 템플릿을 원격 서버에 자동 업로드
- 🎯 **트래픽 제어**: 화이트/블랙 모드로 광고 트래픽 분기
- 🧹 **파일 최적화**: HTML 정리, 폴더 구조 최적화
- 🔒 **보안 설정**: 방화벽 설정, 권한 관리 자동화

## 🛠️ 기술 스택

- **Python**: 3.8+
- **Flask**: 웹 애플리케이션 프레임워크
- **paramiko**: SSH 연결 및 파일 전송
- **nginx**: 웹 서버
- **Let's Encrypt**: SSL 인증서
- **PyQt5**: 크로스 플랫폼 GUI 프레임워크
- **PyInstaller**: 실행 파일 생성

## 📦 배포 파일

### macOS용
- **DMG 파일**: `SiteCreator_macOS.dmg` (74.7 MB)
- **설치 방법**: 더블클릭 → Applications 폴더로 드래그

### Windows용
- **EXE 파일**: Windows에서 `build_windows_only.py` 실행하여 생성
- **설치 방법**: 더블클릭으로 실행 (Python 설치 불필요)

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**Site Creator**로 웹사이트 배포를 간단하고 효율적으로 만들어보세요! 🚀
