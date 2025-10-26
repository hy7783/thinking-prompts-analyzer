#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thinking Prompts Analyzer - Web Application
FastAPI 기반 웹 인터페이스
"""

from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import uuid
import shutil
from datetime import datetime
from pathlib import Path
import asyncio

from input_processor import InputProcessor
from analysis_engine import ThinkingPromptsEngine
from report_generator import ReportGenerator

# FastAPI 앱 초기화
app = FastAPI(
    title="Thinking Prompts Analyzer",
    description="10가지 사고 프롬프트를 활용한 AI 기반 다각도 분석 시스템",
    version="1.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 작업 디렉토리 설정
UPLOAD_DIR = Path("/home/ubuntu/uploads")
REPORT_DIR = Path("/home/ubuntu/reports")
UPLOAD_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# 분석 작업 상태 저장
analysis_jobs = {}

# 시스템 초기화
input_processor = InputProcessor()
analysis_engine = ThinkingPromptsEngine()
report_generator = ReportGenerator()


@app.get("/", response_class=HTMLResponse)
async def root():
    """메인 페이지"""
    return FileResponse("/home/ubuntu/static/index.html")


@app.get("/api/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0"
    }


@app.post("/api/analyze/text")
async def analyze_text(
    background_tasks: BackgroundTasks,
    text: str = Form(...),
    format: str = Form("pdf")
):
    """텍스트 직접 입력 분석"""
    job_id = str(uuid.uuid4())
    
    # 작업 상태 초기화
    analysis_jobs[job_id] = {
        "status": "queued",
        "progress": 0,
        "message": "분석 대기 중...",
        "created_at": datetime.now().isoformat()
    }
    
    # 백그라운드 작업으로 분석 실행
    background_tasks.add_task(
        run_analysis,
        job_id=job_id,
        input_data=text,
        input_type="text",
        output_format=format
    )
    
    return {
        "job_id": job_id,
        "message": "분석이 시작되었습니다."
    }


@app.post("/api/analyze/url")
async def analyze_url(
    background_tasks: BackgroundTasks,
    url: str = Form(...),
    format: str = Form("pdf")
):
    """URL 분석"""
    job_id = str(uuid.uuid4())
    
    analysis_jobs[job_id] = {
        "status": "queued",
        "progress": 0,
        "message": "분석 대기 중...",
        "created_at": datetime.now().isoformat()
    }
    
    background_tasks.add_task(
        run_analysis,
        job_id=job_id,
        input_data=url,
        input_type="url",
        output_format=format
    )
    
    return {
        "job_id": job_id,
        "message": "분석이 시작되었습니다."
    }


@app.post("/api/analyze/file")
async def analyze_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    format: str = Form("pdf")
):
    """파일 업로드 분석"""
    job_id = str(uuid.uuid4())
    
    # 파일 저장
    file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    analysis_jobs[job_id] = {
        "status": "queued",
        "progress": 0,
        "message": "분석 대기 중...",
        "created_at": datetime.now().isoformat(),
        "file_path": str(file_path)
    }
    
    background_tasks.add_task(
        run_analysis,
        job_id=job_id,
        input_data=str(file_path),
        input_type="pdf",
        output_format=format
    )
    
    return {
        "job_id": job_id,
        "message": "파일이 업로드되었습니다. 분석을 시작합니다."
    }


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """분석 상태 조회"""
    if job_id not in analysis_jobs:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다.")
    
    return analysis_jobs[job_id]


@app.get("/api/download/{job_id}")
async def download_report(job_id: str):
    """보고서 다운로드"""
    if job_id not in analysis_jobs:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다.")
    
    job = analysis_jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="분석이 아직 완료되지 않았습니다.")
    
    report_path = job.get("report_path")
    if not report_path or not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="보고서 파일을 찾을 수 없습니다.")
    
    # 파일 확장자에 따라 미디어 타입 설정
    if report_path.endswith(".pdf"):
        media_type = "application/pdf"
        filename = f"analysis_report_{job_id[:8]}.pdf"
    else:
        media_type = "text/markdown"
        filename = f"analysis_report_{job_id[:8]}.md"
    
    return FileResponse(
        report_path,
        media_type=media_type,
        filename=filename
    )


async def run_analysis(job_id: str, input_data: str, input_type: str, output_format: str):
    """백그라운드 분석 작업"""
    try:
        # 1. 입력 처리
        analysis_jobs[job_id].update({
            "status": "processing",
            "progress": 10,
            "message": "입력 데이터 처리 중..."
        })
        
        processed_input = input_processor.process(input_data, input_type)
        
        # 2. 10가지 프롬프트 분석
        analysis_jobs[job_id].update({
            "progress": 20,
            "message": "10가지 사고 프롬프트 분석 중..."
        })
        
        def progress_callback(current, total, title):
            progress = 20 + int((current / total) * 60)
            analysis_jobs[job_id].update({
                "progress": progress,
                "message": f"[{current}/{total}] {title} 분석 중..."
            })
        
        analysis_results = analysis_engine.analyze(
            processed_input['content'],
            progress_callback=progress_callback
        )
        
        # 3. 종합 요약 생성
        analysis_jobs[job_id].update({
            "progress": 85,
            "message": "종합 요약 생성 중..."
        })
        
        synthesis = analysis_engine.generate_summary(analysis_results)
        
        # 4. 보고서 생성
        analysis_jobs[job_id].update({
            "progress": 90,
            "message": "보고서 생성 중..."
        })
        
        report_path = report_generator.generate_report(
            processed_input,
            analysis_results,
            synthesis,
            output_format=output_format
        )
        
        # 보고서를 reports 디렉토리로 이동
        final_report_path = REPORT_DIR / f"{job_id}_report.{output_format}"
        shutil.move(report_path, final_report_path)
        
        # 완료
        analysis_jobs[job_id].update({
            "status": "completed",
            "progress": 100,
            "message": "분석 완료!",
            "report_path": str(final_report_path),
            "completed_at": datetime.now().isoformat()
        })
        
    except Exception as e:
        analysis_jobs[job_id].update({
            "status": "failed",
            "progress": 0,
            "message": f"오류 발생: {str(e)}",
            "error": str(e)
        })


@app.get("/api/prompts")
async def get_prompts():
    """10가지 프롬프트 정보 조회"""
    prompts = analysis_engine.get_all_prompts()
    return {
        "prompts": [
            {
                "key": key,
                "title": info["title"],
                "title_en": info["title_en"],
                "description": info["description"]
            }
            for key, info in prompts.items()
        ]
    }


# 정적 파일 서빙 (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="/home/ubuntu/static"), name="static")


if __name__ == "__main__":
    uvicorn.run(
        "web_app:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )

