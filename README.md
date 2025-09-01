# SiteCreator

웹사이트 생성 도구입니다.

## 🚀 빠른 시작

### 필수 요구사항
- Python 3.9 이상
- pip (Python 패키지 관리자)

### 설치 및 실행

1. **저장소 클론**
```bash
git clone <repository-url>
cd sitecreator
```

2. **가상환경 생성 및 활성화**
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **의존성 설치**
```bash
pip install -r requirements.txt
```

4. **애플리케이션 실행**
```bash
python ui.py
```

## 📁 프로젝트 구조

- `ui.py` - 메인 GUI 애플리케이션
- `server.py` - 웹 서버
- `page_default/` - 기본 페이지 템플릿
- `requirements.txt` - Python 의존성 목록

## 🔧 개발 환경 설정

개발 모드로 실행하려면:
```bash
python dev_run.py
```

## 📦 배포

### macOS
```bash
python build_macos.py
```

### Windows
```bash
python build_windows_complete.py
```

## 📚 자세한 사용법

자세한 사용법은 `USER_MANUAL.md` 파일을 참조하세요.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
