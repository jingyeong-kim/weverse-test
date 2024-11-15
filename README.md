# weverse-test Project

## 프로젝트 구조

```plaintext
weverse-test/
├── .venv/                    # Python 가상 환경 디렉토리
├── core/                     # 코어 모듈: 드라이버 설정, 유틸리티, Slack API 연동 등
│   ├── driver.py             # Selenium WebDriver 설정 모듈
│   ├── slack.py              # Slack API를 활용한 인증 URL 추출 모듈
│   ├── utils.py              # 공통 유틸리티 함수 (예: 랜덤 이메일 생성, 스크린샷 저장 등)
│   └── __init__.py           # 패키지 초기화 파일
├── pages/                    # 페이지 객체 모델(Page Object Model) 디렉토리
│   ├── home_page.py          # 홈 페이지에 대한 페이지 객체 클래스
│   ├── profile_page.py       # 프로필 페이지에 대한 페이지 객체 클래스
│   ├── signup/               # 회원가입 관련 페이지 객체들
│   │   ├── agreement_page.py # 약관 동의 페이지 객체 클래스
│   │   ├── login_page.py     # 로그인 페이지 객체 클래스
│   │   ├── nickname_page.py  # 닉네임 설정 페이지 객체 클래스
│   │   ├── password_page.py  # 비밀번호 설정 페이지 객체 클래스
│   │   ├── signup_page.py    # 회원가입 초기 단계 페이지 객체 클래스
│   │   └── __init__.py       # 패키지 초기화 파일
│   └── __init__.py           # 패키지 초기화 파일
├── tests/                    # 테스트 스크립트 디렉토리
│   ├── conftest.py           # 공통 테스트 설정 (pytest 픽스처 등)
│   ├── screenshots/          # 테스트 실패 시 저장되는 스크린샷 폴더
│   ├── test_login_profile.py # 로그인 후 프로필 페이지 접근 테스트 스크립트
│   ├── test_signup_certification.py  # 회원 가입 후 이메일 인증 테스트 스크립트
│   ├── test_user_signup.py    # 회원 가입 테스트 스크립트 (이메일 미인증)
│   └── __init__.py           # 패키지 초기화 파일
└── .env                      # 환경 변수 설정 파일 (Slack API 토큰, 테스트 사용자 정보 등)
```

## 가상 환경 설정

```plaintext
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

