# 🧠 Thinking Prompts Analyzer

AI 기반 10가지 사고 프롬프트를 활용한 다각도 분석 시스템

## 🌟 주요 기능

- **텍스트 직접 입력** - 아이디어, 계획, 전략 분석
- **URL 분석** - 웹 페이지, 논문, 저널 자동 크롤링
- **PDF 파일 업로드** - 문서 파일 분석
- **10가지 사고 프롬프트** - 다각도 AI 분석
- **전문 보고서 생성** - PDF/Markdown 형식
- **모바일 최적화** - 반응형 웹 디자인

## 🚀 배포 방법

### Railway 배포

1. [Railway](https://railway.app) 계정 생성
2. GitHub 리포지토리 연결
3. 환경 변수 설정:
   - `OPENAI_API_KEY`: OpenAI API 키
4. 자동 배포 완료

### Render 배포

1. [Render](https://render.com) 계정 생성
2. New Web Service 선택
3. GitHub 리포지토리 연결
4. 설정:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn web_app:app --host 0.0.0.0 --port $PORT`
5. 환경 변수 추가: `OPENAI_API_KEY`

### 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
export OPENAI_API_KEY="your-api-key"

# 서버 실행
python web_app.py
```

브라우저에서 `http://localhost:8000` 접속

## 📋 환경 변수

| 변수명 | 설명 | 필수 |
|--------|------|------|
| `OPENAI_API_KEY` | OpenAI API 키 | ✅ |
| `PORT` | 서버 포트 (기본값: 8000) | ❌ |

## 🎯 10가지 사고 프롬프트

1. **내 사고에 도전하기** - 비판적 사고를 통한 가정과 논리 검증
2. **다른 렌즈로 재구성하기** - 새로운 관점에서 아이디어 재해석
3. **더 깊은 질문 발견하기** - 표면적 문제 뒤의 본질적 질문 찾기
4. **직관을 언어화하기** - 막연한 느낌을 구체적 언어로 전환
5. **2차, 3차 효과 찾기** - 결정의 장기적 파급효과 분석
6. **보이지 않는 변수 발견하기** - 간과된 핵심 변수 식별
7. **핵심 원리 추출하기** - 재사용 가능한 원리 도출
8. **직관을 역설계하기** - 직관적 판단의 논리적 근거 분석
9. **숨겨진 패턴 찾기** - 여러 사례를 연결하는 공통 패턴 발견
10. **역방향 사고** - 목표에서 현재로 역추적하여 필요조건 도출

## 🔧 기술 스택

- **Backend**: FastAPI, Python 3.11
- **AI**: OpenAI GPT-4.1-mini
- **Frontend**: HTML5, CSS3, JavaScript
- **Server**: Uvicorn (ASGI)

## 📦 프로젝트 구조

```
thinking-analyzer-deploy/
├── web_app.py              # FastAPI 메인 서버
├── input_processor.py      # 입력 처리 모듈
├── analysis_engine.py      # AI 분석 엔진
├── report_generator.py     # 보고서 생성 모듈
├── static/
│   └── index.html         # 웹 프론트엔드
├── requirements.txt        # Python 의존성
├── Procfile               # 배포 설정
├── runtime.txt            # Python 버전
└── README.md              # 프로젝트 문서
```

## 📱 모바일 지원

- ✅ 반응형 웹 디자인
- ✅ 터치 친화적 인터페이스
- ✅ 모든 화면 크기 지원
- ✅ iOS/Android 브라우저 최적화

## 🎨 UI/UX 특징

- **미니멀 디자인** - 깔끔한 흰색 배경
- **직관적 인터페이스** - 3단계 분석 프로세스
- **실시간 피드백** - 진행 상황 표시
- **명확한 계층** - 정보 구조화

## 📄 라이선스

MIT License

## 🤝 기여

이슈와 풀 리퀘스트를 환영합니다!

## 📧 문의

프로젝트 관련 문의사항은 이슈를 통해 남겨주세요.

---

**Thinking Prompts Analyzer** - AI 기반 다각도 분석 시스템

