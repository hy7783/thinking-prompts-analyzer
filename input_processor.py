#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
입력 처리 모듈 (Input Processor)
다양한 형식의 입력(텍스트, URL, PDF)을 통합된 텍스트로 변환
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import PyPDF2
import pdfplumber


class InputProcessor:
    """입력 데이터를 처리하여 통합된 텍스트로 변환하는 클래스"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def process(self, input_data, input_type='auto'):
        """
        입력 데이터를 처리하여 텍스트 추출
        
        Args:
            input_data: 입력 데이터 (텍스트, URL, 파일 경로)
            input_type: 'auto', 'text', 'url', 'pdf'
        
        Returns:
            dict: {
                'content': 추출된 텍스트,
                'metadata': 메타데이터 (제목, 출처 등),
                'type': 입력 타입
            }
        """
        if input_type == 'auto':
            input_type = self._detect_input_type(input_data)
        
        if input_type == 'url':
            return self._process_url(input_data)
        elif input_type == 'pdf':
            return self._process_pdf(input_data)
        else:  # text
            return self._process_text(input_data)
    
    def _detect_input_type(self, input_data):
        """입력 타입 자동 감지"""
        # URL 패턴 체크
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if url_pattern.match(str(input_data)):
            return 'url'
        
        # 파일 경로 체크
        if isinstance(input_data, str) and os.path.isfile(input_data):
            if input_data.lower().endswith('.pdf'):
                return 'pdf'
        
        # 기본값: 텍스트
        return 'text'
    
    def _process_text(self, text):
        """텍스트 입력 처리"""
        return {
            'content': text.strip(),
            'metadata': {
                'title': self._extract_title_from_text(text),
                'source': 'Direct Input',
                'length': len(text)
            },
            'type': 'text'
        }
    
    def _process_url(self, url):
        """URL 입력 처리 - 웹 페이지 크롤링"""
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 제목 추출
            title = self._extract_title_from_html(soup)
            
            # 본문 추출
            content = self._extract_content_from_html(soup)
            
            return {
                'content': content,
                'metadata': {
                    'title': title,
                    'source': url,
                    'domain': urlparse(url).netloc,
                    'length': len(content)
                },
                'type': 'url'
            }
        
        except Exception as e:
            raise Exception(f"URL 처리 중 오류 발생: {str(e)}")
    
    def _process_pdf(self, pdf_path):
        """PDF 파일 처리 - 텍스트 추출"""
        try:
            content = ""
            metadata = {
                'title': os.path.basename(pdf_path),
                'source': pdf_path,
                'pages': 0
            }
            
            # pdfplumber를 우선 사용 (더 정확한 텍스트 추출)
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    metadata['pages'] = len(pdf.pages)
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            content += text + "\n\n"
            except:
                # pdfplumber 실패 시 PyPDF2 사용
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    metadata['pages'] = len(pdf_reader.pages)
                    for page in pdf_reader.pages:
                        content += page.extract_text() + "\n\n"
            
            # PDF 메타데이터 추출 시도
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    if pdf_reader.metadata:
                        if '/Title' in pdf_reader.metadata:
                            metadata['title'] = pdf_reader.metadata['/Title']
                        if '/Author' in pdf_reader.metadata:
                            metadata['author'] = pdf_reader.metadata['/Author']
            except:
                pass
            
            metadata['length'] = len(content)
            
            return {
                'content': content.strip(),
                'metadata': metadata,
                'type': 'pdf'
            }
        
        except Exception as e:
            raise Exception(f"PDF 처리 중 오류 발생: {str(e)}")
    
    def _extract_title_from_html(self, soup):
        """HTML에서 제목 추출"""
        # <title> 태그
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        
        # <h1> 태그
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        
        # og:title 메타 태그
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()
        
        return "Untitled"
    
    def _extract_content_from_html(self, soup):
        """HTML에서 본문 추출"""
        # 불필요한 태그 제거
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()
        
        # article 태그 우선 검색
        article = soup.find('article')
        if article:
            return self._clean_text(article.get_text())
        
        # main 태그 검색
        main = soup.find('main')
        if main:
            return self._clean_text(main.get_text())
        
        # div.content, div.article 등 검색
        content_div = soup.find('div', class_=re.compile(r'content|article|post|entry', re.I))
        if content_div:
            return self._clean_text(content_div.get_text())
        
        # 전체 body 사용
        body = soup.find('body')
        if body:
            return self._clean_text(body.get_text())
        
        return self._clean_text(soup.get_text())
    
    def _clean_text(self, text):
        """텍스트 정리"""
        # 연속된 공백 제거
        text = re.sub(r'\s+', ' ', text)
        # 연속된 줄바꿈 제거
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()
    
    def _extract_title_from_text(self, text):
        """텍스트에서 제목 추출 (첫 줄 또는 첫 문장)"""
        lines = text.strip().split('\n')
        if lines:
            first_line = lines[0].strip()
            # 첫 줄이 너무 길면 첫 50자만
            if len(first_line) > 50:
                return first_line[:50] + "..."
            return first_line
        return "Untitled"


# 테스트 코드
if __name__ == "__main__":
    processor = InputProcessor()
    
    # 텍스트 입력 테스트
    text_input = """
    AI 기반 교육 플랫폼 개발 계획
    
    우리는 개인화된 학습 경험을 제공하는 AI 교육 플랫폼을 개발하려고 합니다.
    주요 기능으로는 학습자 수준 분석, 맞춤형 콘텐츠 추천, 실시간 피드백 제공이 있습니다.
    """
    
    result = processor.process(text_input)
    print("=== 텍스트 입력 테스트 ===")
    print(f"타입: {result['type']}")
    print(f"제목: {result['metadata']['title']}")
    print(f"내용 길이: {result['metadata']['length']}자")
    print(f"내용 미리보기: {result['content'][:100]}...")
    print()

