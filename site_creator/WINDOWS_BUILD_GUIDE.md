# 🪟 Windows EXE 파일 생성 가이드

**Site Creator를 Windows 실행 파일로 만들기**

## 🚀 빠른 시작

### 1단계: 파일 다운로드
```cmd
# 프로젝트 폴더로 이동
cd C:\path\to\sitecreator\site_creator
```

### 2단계: 자동 빌드 실행
```cmd
# 통합 빌드 스크립트 실행 (권장)
build_windows_complete.bat
```

### 3단계: EXE 파일 확인
```
📁 dist\SiteCreator.exe
```

## 📋 시스템 요구사항

### 필수 소프트웨어
- **Windows**: 10/11 (64비트 권장)
- **Python**: 3.8 이상
- **메모리**: 최소 4GB RAM
- **디스크**: 최소 2GB 여유 공간

### 권장 사양
- **Windows**: 11 (64비트)
- **Python**: 3.11 이상
- **메모리**: 8GB RAM 이상
- **디스크**: 5GB 여유 공간
- **CPU**: 4코어 이상

## 🔧 수동 빌드 방법

### 1. Python 환경 설정
```cmd
# Python 버전 확인
python --version

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate.bat
```

### 2. 의존성 설치
```cmd
# pip 업그레이드
python -m pip install --upgrade pip

# 필수 패키지 설치
pip install -r requirements.txt

# PyInstaller 설치
pip install pyinstaller

# 아이콘 생성용 Pillow 설치
pip install Pillow
```

### 3. 아이콘 생성
```cmd
# Windows용 아이콘 생성
python create_icon.py
```

### 4. EXE 파일 생성
```cmd
# Windows EXE 빌드
python build_windows_only.py
```

## 📁 생성되는 파일들

### 빌드 결과물
```
dist/
└── SiteCreator.exe          # Windows 실행 파일 (50-100MB)
```

### 빌드 과정 파일들
```
build/                       # PyInstaller 빌드 폴더
├── SiteCreator/            # 임시 빌드 파일들
└── *.spec                  # 빌드 설정 파일

SiteCreator.spec            # PyInstaller 스펙 파일
icon.ico                    # Windows 아이콘 파일
```

## ⚠️ 주의사항

### 빌드 과정
- **시간**: 5-15분 소요 (컴퓨터 성능에 따라)
- **인터넷**: 의존성 다운로드 시 필요
- **방화벽**: Windows Defender가 PyInstaller를 차단할 수 있음

### 실행 파일 특징
- **크기**: 50-100MB (모든 의존성 포함)
- **독립성**: Python 설치 불필요
- **호환성**: Windows 10/11 (64비트)
- **보안**: 코드 서명 없음 (Windows SmartScreen 경고 가능)

## 🆘 문제 해결

### 일반적인 오류들

#### 1. Python 설치 오류
```cmd
# Python이 설치되지 않은 경우
# https://python.org 에서 다운로드
# 설치 시 "Add Python to PATH" 체크
```

#### 2. 가상환경 활성화 오류
```cmd
# PowerShell 정책 문제인 경우
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 또는 cmd 사용
cmd /k "venv\Scripts\activate.bat"
```

#### 3. PyInstaller 오류
```cmd
# 기존 설치 제거 후 재설치
pip uninstall pyinstaller
pip install pyinstaller

# 또는 특정 버전 설치
pip install pyinstaller==5.13.0
```

#### 4. 메모리 부족 오류
```cmd
# 가상 메모리 증가
# 시스템 속성 > 고급 > 성능 설정 > 고급 > 가상 메모리
```

### 디버깅 모드
```cmd
# 상세한 빌드 정보 출력
pyinstaller --debug=all --onefile --windowed ui.py
```

## 🎯 최적화 팁

### 빌드 속도 향상
```cmd
# 병렬 빌드 활성화
pyinstaller --onefile --windowed --jobs=4 ui.py

# 캐시 사용
pyinstaller --onefile --windowed --cache-path=cache ui.py
```

### 파일 크기 최적화
```cmd
# UPX 압축 사용 (별도 설치 필요)
pyinstaller --onefile --windowed --upx-dir=upx ui.py

# 불필요한 모듈 제외
pyinstaller --onefile --windowed --exclude-module=tkinter ui.py
```

## 📞 지원 및 문의

### 문제 발생 시
1. **터미널 오류 메시지** 복사
2. **Python 버전** 확인
3. **Windows 버전** 확인
4. **메모리 사용량** 확인

### 추가 도움
- **GitHub Issues**: 프로젝트 저장소에 문제 등록
- **문서 참조**: `USER_MANUAL.md` 확인
- **커뮤니티**: 개발자 포럼 활용

---

**💡 팁**: `build_windows_complete.bat`를 사용하면 모든 과정이 자동으로 처리됩니다!
