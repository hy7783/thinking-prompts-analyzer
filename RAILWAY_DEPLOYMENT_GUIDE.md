# 🚂 Railway 배포 가이드

## Railway를 통한 영구 배포 방법

Railway는 무료 티어를 제공하는 클라우드 플랫폼으로, FastAPI 애플리케이션을 쉽게 배포할 수 있습니다.

---

## 📋 사전 준비

### 1. 필요한 계정
- [Railway](https://railway.app) 계정
- [GitHub](https://github.com) 계정

### 2. OpenAI API 키
- [OpenAI Platform](https://platform.openai.com/api-keys)에서 API 키 발급
- 분석 엔진에 필수적으로 필요합니다

---

## 🚀 배포 단계별 가이드

### Step 1: GitHub 리포지토리 생성

1. **GitHub에 로그인**
2. **New Repository 클릭**
3. **리포지토리 정보 입력**
   - Repository name: `thinking-prompts-analyzer`
   - Description: `AI-powered multi-perspective analysis system`
   - Public 또는 Private 선택
4. **Create repository 클릭**

### Step 2: 코드 푸시

다운로드한 `thinking-analyzer-deploy.tar.gz` 파일을 압축 해제 후:

```bash
# 압축 해제
tar -xzf thinking-analyzer-deploy.tar.gz
cd thinking-analyzer-deploy

# GitHub 리포지토리와 연결
git remote add origin https://github.com/YOUR_USERNAME/thinking-prompts-analyzer.git

# 브랜치 이름 변경 (선택사항)
git branch -M main

# 코드 푸시
git push -u origin main
```

### Step 3: Railway 프로젝트 생성

1. **Railway 접속**
   - https://railway.app 방문
   - "Start a New Project" 클릭

2. **GitHub 연결**
   - "Deploy from GitHub repo" 선택
   - GitHub 계정 인증
   - `thinking-prompts-analyzer` 리포지토리 선택

3. **자동 감지**
   - Railway가 자동으로 Python 프로젝트 감지
   - `requirements.txt`와 `Procfile` 자동 인식

### Step 4: 환경 변수 설정

1. **Variables 탭 클릭**
2. **New Variable 클릭**
3. **환경 변수 추가**:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

4. **저장 및 재배포**

### Step 5: 배포 완료

- Railway가 자동으로 빌드 및 배포 시작
- 약 3-5분 소요
- 배포 완료 후 공개 URL 생성

---

## 🔗 공개 URL 설정

### 도메인 생성

1. **Settings 탭 클릭**
2. **Networking 섹션**
3. **Generate Domain 클릭**
4. **자동 생성된 URL 확인**
   - 예: `thinking-analyzer-production.up.railway.app`

### 커스텀 도메인 (선택사항)

1. **Custom Domain 추가**
2. **본인 소유 도메인 연결**
3. **DNS 설정 완료**

---

## 📊 무료 티어 제한

Railway 무료 티어:
- ✅ **$5 무료 크레딧** (매월)
- ✅ **500시간 실행 시간**
- ✅ **무제한 프로젝트**
- ✅ **자동 배포**
- ✅ **SSL 인증서 자동 발급**

### 비용 최적화
- 사용하지 않을 때 자동 슬립
- 요청 시 자동 웨이크업
- 효율적인 리소스 사용

---

## 🔄 자동 배포 설정

### GitHub 연동 후

1. **코드 수정 후 푸시**
```bash
git add .
git commit -m "Update feature"
git push
```

2. **Railway 자동 감지**
   - 새 커밋 감지
   - 자동 빌드 시작
   - 자동 배포 완료

3. **배포 로그 확인**
   - Deployments 탭에서 실시간 로그 확인

---

## 🐛 트러블슈팅

### 문제 1: 빌드 실패

**증상**: Requirements 설치 실패

**해결**:
```bash
# requirements.txt 버전 확인
# 호환되지 않는 패키지 버전 수정
```

### 문제 2: 환경 변수 오류

**증상**: OpenAI API 키 인식 안 됨

**해결**:
1. Variables 탭에서 `OPENAI_API_KEY` 확인
2. 값이 올바른지 검증
3. 재배포 (Redeploy)

### 문제 3: 포트 바인딩 오류

**증상**: 서버가 시작되지 않음

**해결**:
- `Procfile`에서 `$PORT` 환경 변수 사용 확인
- Railway가 자동으로 포트 할당

### 문제 4: 메모리 초과

**증상**: 앱이 크래시됨

**해결**:
- 무료 티어 메모리 제한 확인
- 코드 최적화 또는 유료 플랜 고려

---

## 📈 모니터링

### Railway 대시보드

1. **Metrics 탭**
   - CPU 사용률
   - 메모리 사용량
   - 네트워크 트래픽

2. **Logs 탭**
   - 실시간 애플리케이션 로그
   - 에러 추적

3. **Deployments 탭**
   - 배포 히스토리
   - 롤백 가능

---

## 🔐 보안 설정

### 환경 변수 보호

- ✅ `.env` 파일은 `.gitignore`에 포함
- ✅ API 키는 Railway Variables에만 저장
- ✅ GitHub에 절대 커밋하지 않기

### API 키 관리

```bash
# .env.example 제공 (실제 값 제외)
OPENAI_API_KEY=your-api-key-here

# 실제 .env는 로컬에만 보관
```

---

## 💰 비용 관리

### 무료 티어 최대 활용

1. **슬립 모드 활용**
   - 15분 비활성 시 자동 슬립
   - 첫 요청 시 웨이크업 (약 5초)

2. **크레딧 모니터링**
   - Railway 대시보드에서 사용량 확인
   - 알림 설정

3. **최적화**
   - 불필요한 로그 제거
   - 효율적인 쿼리 사용

---

## 🎯 배포 체크리스트

### 배포 전
- [ ] GitHub 리포지토리 생성
- [ ] 코드 푸시 완료
- [ ] OpenAI API 키 준비
- [ ] `.env.example` 확인

### 배포 중
- [ ] Railway 프로젝트 생성
- [ ] GitHub 연동
- [ ] 환경 변수 설정
- [ ] 빌드 성공 확인

### 배포 후
- [ ] 공개 URL 접속 테스트
- [ ] 텍스트 분석 테스트
- [ ] URL 분석 테스트
- [ ] 파일 업로드 테스트
- [ ] 모바일 접속 테스트

---

## 🌐 배포 완료 후

### 공개 URL 공유

배포 완료 후 생성된 URL:
```
https://your-app-name.up.railway.app
```

### 테스트

1. **브라우저에서 접속**
2. **샘플 텍스트로 분석 실행**
3. **보고서 다운로드 확인**

### 홍보

- 소셜 미디어 공유
- 문서에 URL 추가
- 사용자 피드백 수집

---

## 📚 추가 리소스

### Railway 문서
- [Railway Docs](https://docs.railway.app)
- [Python 배포 가이드](https://docs.railway.app/guides/python)
- [환경 변수 설정](https://docs.railway.app/develop/variables)

### 커뮤니티
- [Railway Discord](https://discord.gg/railway)
- [Railway Forum](https://help.railway.app)

---

## 🎉 축하합니다!

Railway를 통한 영구 배포가 완료되었습니다!

이제 전 세계 어디서나 접속 가능한 웹 애플리케이션이 되었습니다.

---

**다음 단계**: 사용자 피드백을 받고 기능을 개선해보세요!

