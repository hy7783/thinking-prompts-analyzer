# 🌐 대체 플랫폼 배포 가이드

Railway 외에도 다양한 무료 클라우드 플랫폼에 배포할 수 있습니다.

---

## 1. 🎨 Render

### 특징
- ✅ 무료 티어 제공
- ✅ 자동 SSL 인증서
- ✅ GitHub 자동 배포
- ✅ 간단한 설정

### 무료 티어
- 750시간/월 무료
- 512MB RAM
- 자동 슬립 (15분 비활성)

### 배포 방법

1. **Render 계정 생성**
   - https://render.com 접속
   - GitHub로 로그인

2. **New Web Service 생성**
   - Dashboard → New → Web Service
   - GitHub 리포지토리 연결

3. **설정**
   ```
   Name: thinking-prompts-analyzer
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn web_app:app --host 0.0.0.0 --port $PORT
   ```

4. **환경 변수**
   - `OPENAI_API_KEY`: 본인의 API 키

5. **배포 시작**
   - Create Web Service 클릭
   - 자동 빌드 및 배포

### 장점
- 매우 간단한 설정
- 안정적인 무료 티어
- 좋은 문서화

### 단점
- 슬립 모드 (웨이크업 시간 약 30초)
- 제한된 리소스

---

## 2. ✈️ Fly.io

### 특징
- ✅ 글로벌 엣지 네트워크
- ✅ 빠른 배포
- ✅ Dockerfile 지원
- ✅ 무료 티어

### 무료 티어
- 3개 공유 CPU
- 256MB RAM × 3
- 3GB 스토리지

### 배포 방법

1. **Fly CLI 설치**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **로그인**
   ```bash
   fly auth login
   ```

3. **앱 초기화**
   ```bash
   cd thinking-analyzer-deploy
   fly launch
   ```

4. **환경 변수 설정**
   ```bash
   fly secrets set OPENAI_API_KEY=your-api-key
   ```

5. **배포**
   ```bash
   fly deploy
   ```

### 장점
- 빠른 글로벌 배포
- 슬립 모드 없음
- 좋은 성능

### 단점
- CLI 사용 필수
- 약간 복잡한 설정

---

## 3. 🔷 Vercel (정적 + Serverless)

### 특징
- ✅ 초고속 배포
- ✅ Serverless Functions
- ✅ 무제한 대역폭
- ✅ 자동 HTTPS

### 제한사항
- FastAPI 전체를 직접 호스팅하기 어려움
- Serverless Functions로 변환 필요

### 배포 방법 (변환 필요)

1. **프론트엔드 배포**
   - `static/index.html`을 Vercel에 배포
   
2. **백엔드를 Serverless Functions로 변환**
   - 각 API 엔드포인트를 개별 함수로 분리
   - `/api` 디렉토리에 배치

3. **배포**
   ```bash
   vercel
   ```

### 장점
- 매우 빠른 속도
- 무제한 대역폭
- 우수한 DX

### 단점
- FastAPI 직접 호스팅 불가
- 코드 구조 변경 필요

---

## 4. 🐳 Heroku (유료 전환)

### 특징
- 🔴 무료 티어 종료 (2022년 11월)
- ✅ 안정적인 플랫폼
- ✅ 다양한 애드온

### 최소 비용
- $7/월 (Eco Dynos)

### 배포 방법

1. **Heroku CLI 설치**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **로그인**
   ```bash
   heroku login
   ```

3. **앱 생성**
   ```bash
   cd thinking-analyzer-deploy
   heroku create thinking-prompts-analyzer
   ```

4. **환경 변수 설정**
   ```bash
   heroku config:set OPENAI_API_KEY=your-api-key
   ```

5. **배포**
   ```bash
   git push heroku main
   ```

### 장점
- 매우 안정적
- 풍부한 애드온
- 좋은 문서

### 단점
- 무료 티어 없음
- 비용 발생

---

## 5. ☁️ Google Cloud Run

### 특징
- ✅ 컨테이너 기반
- ✅ 사용한 만큼만 과금
- ✅ 자동 스케일링
- ✅ 무료 티어

### 무료 티어
- 월 200만 요청
- 360,000 GB-초 메모리
- 180,000 vCPU-초

### 배포 방법

1. **Dockerfile 생성**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD uvicorn web_app:app --host 0.0.0.0 --port $PORT
   ```

2. **gcloud CLI 설치**
   ```bash
   curl https://sdk.cloud.google.com | bash
   ```

3. **프로젝트 설정**
   ```bash
   gcloud init
   gcloud config set project YOUR_PROJECT_ID
   ```

4. **배포**
   ```bash
   gcloud run deploy thinking-analyzer \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

5. **환경 변수**
   - Cloud Console에서 설정

### 장점
- 강력한 인프라
- 자동 스케일링
- 무료 티어 넉넉함

### 단점
- 복잡한 설정
- GCP 계정 필요

---

## 6. 🔵 Azure App Service

### 특징
- ✅ Microsoft 클라우드
- ✅ 무료 티어 (F1)
- ✅ CI/CD 통합
- ✅ 다양한 언어 지원

### 무료 티어
- 1GB 메모리
- 1GB 스토리지
- 60분/일 CPU 시간

### 배포 방법

1. **Azure CLI 설치**
   ```bash
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

2. **로그인**
   ```bash
   az login
   ```

3. **리소스 그룹 생성**
   ```bash
   az group create --name thinking-analyzer-rg --location eastus
   ```

4. **App Service 계획 생성**
   ```bash
   az appservice plan create \
     --name thinking-analyzer-plan \
     --resource-group thinking-analyzer-rg \
     --sku F1 \
     --is-linux
   ```

5. **웹 앱 생성**
   ```bash
   az webapp create \
     --resource-group thinking-analyzer-rg \
     --plan thinking-analyzer-plan \
     --name thinking-prompts-analyzer \
     --runtime "PYTHON:3.11"
   ```

6. **배포**
   ```bash
   az webapp up --name thinking-prompts-analyzer
   ```

### 장점
- Microsoft 생태계 통합
- 안정적인 서비스
- 무료 티어 제공

### 단점
- 복잡한 설정
- 제한된 무료 리소스

---

## 📊 플랫폼 비교표

| 플랫폼 | 무료 티어 | 슬립 모드 | 설정 난이도 | 추천도 |
|--------|-----------|-----------|-------------|--------|
| **Railway** | ✅ $5/월 | ❌ | ⭐ 쉬움 | ⭐⭐⭐⭐⭐ |
| **Render** | ✅ 750h/월 | ✅ 15분 | ⭐ 쉬움 | ⭐⭐⭐⭐ |
| **Fly.io** | ✅ 제한적 | ❌ | ⭐⭐ 보통 | ⭐⭐⭐⭐ |
| **Vercel** | ✅ 무제한 | ❌ | ⭐⭐⭐ 어려움 | ⭐⭐⭐ |
| **Heroku** | ❌ 유료 | - | ⭐ 쉬움 | ⭐⭐ |
| **Cloud Run** | ✅ 넉넉함 | ❌ | ⭐⭐⭐ 어려움 | ⭐⭐⭐⭐ |
| **Azure** | ✅ 제한적 | ❌ | ⭐⭐⭐ 어려움 | ⭐⭐⭐ |

---

## 🎯 추천 플랫폼

### 초보자
→ **Railway** 또는 **Render**
- 가장 간단한 설정
- 좋은 무료 티어
- 빠른 배포

### 성능 중시
→ **Fly.io** 또는 **Cloud Run**
- 슬립 모드 없음
- 빠른 응답 속도
- 글로벌 배포

### 기업용
→ **Heroku** 또는 **Azure**
- 안정적인 서비스
- 풍부한 기능
- 전문 지원

---

## 🔄 마이그레이션

### 플랫폼 간 이동

모든 플랫폼이 동일한 코드베이스를 사용하므로:

1. **새 플랫폼에서 프로젝트 생성**
2. **GitHub 리포지토리 연결**
3. **환경 변수 설정**
4. **배포**

### 다운타임 최소화

1. **새 플랫폼에 먼저 배포**
2. **테스트 완료**
3. **DNS 변경 또는 URL 업데이트**
4. **이전 플랫폼 종료**

---

## 💡 팁

### 1. 여러 플랫폼 동시 사용
- 무료 티어 한도를 늘리기 위해
- 백업 서버로 활용
- A/B 테스트

### 2. 모니터링
- UptimeRobot으로 다운타임 감지
- 여러 플랫폼 상태 확인

### 3. 비용 최적화
- 무료 티어 최대 활용
- 사용량 모니터링
- 필요시 플랫폼 전환

---

## 📚 추가 리소스

- [Railway vs Render 비교](https://railway.app/vs/render)
- [Fly.io 문서](https://fly.io/docs/)
- [Google Cloud Run 가이드](https://cloud.google.com/run/docs)
- [Azure App Service 문서](https://docs.microsoft.com/azure/app-service/)

---

**선택은 여러분의 필요에 따라!** 🚀

