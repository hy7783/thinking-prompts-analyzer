#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
보고서 생성 모듈 (Report Generator)
분석 결과를 구조화된 마크다운 및 PDF 보고서로 변환
"""

import os
from datetime import datetime
import markdown


class ReportGenerator:
    """분석 결과를 PDF 보고서로 생성하는 클래스"""
    
    def __init__(self):
        self.report_template = """# {title}

**분석 일시**: {timestamp}  
**출처**: {source}  
**분석 유형**: {input_type}

---

## 📋 요약 (Executive Summary)

{summary}

---

## 📄 원본 내용 (Original Content)

{original_content}

---

## 🧠 10가지 관점별 분석

{analyses}

---

## 🎯 종합 결론 (Synthesis)

{synthesis}

---

## 📚 참고 정보

- **분석 모델**: GPT-4.1-mini
- **분석 프레임워크**: 10가지 사고 지원 프롬프트
- **생성 시스템**: Thinking Prompts Analysis System v1.0
- **보고서 생성 일시**: {report_timestamp}

---

*본 보고서는 AI 기반 다각도 사고 분석 시스템을 통해 자동 생성되었습니다.*
"""
    
    def generate_report(self, input_data, analysis_results, synthesis, output_format='markdown'):
        """
        분석 결과를 보고서로 생성
        
        Args:
            input_data: InputProcessor의 출력 (dict)
            analysis_results: ThinkingPromptsEngine의 분석 결과 (dict)
            synthesis: 종합 요약 (str)
            output_format: 'markdown' 또는 'pdf'
        
        Returns:
            str: 생성된 보고서 파일 경로
        """
        # 메타데이터 추출
        metadata = input_data.get('metadata', {})
        title = metadata.get('title', 'Untitled Analysis')
        source = metadata.get('source', 'Unknown')
        input_type = input_data.get('type', 'text')
        original_content = input_data.get('content', '')
        
        # 타임스탬프
        timestamp = datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')
        
        # 요약 생성 (첫 500자)
        summary = self._generate_summary(original_content, analysis_results)
        
        # 분석 결과 포맷팅
        analyses = self._format_analyses(analysis_results)
        
        # 보고서 내용 생성
        report_content = self.report_template.format(
            title=title,
            timestamp=timestamp,
            source=source,
            input_type=self._format_input_type(input_type),
            summary=summary,
            original_content=self._truncate_content(original_content, 2000),
            analyses=analyses,
            synthesis=synthesis,
            report_timestamp=timestamp
        )
        
        # 파일명 생성
        safe_title = self._sanitize_filename(title)
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if output_format == 'markdown':
            output_path = f"/home/ubuntu/report_{safe_title}_{timestamp_str}.md"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            return output_path
        
        elif output_format == 'pdf':
            # 먼저 마크다운 파일 생성
            md_path = f"/home/ubuntu/report_{safe_title}_{timestamp_str}.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            # PDF로 변환
            pdf_path = f"/home/ubuntu/report_{safe_title}_{timestamp_str}.pdf"
            self._convert_to_pdf(md_path, pdf_path)
            
            return pdf_path
        
        else:
            raise ValueError(f"지원하지 않는 출력 형식: {output_format}")
    
    def _generate_summary(self, content, analysis_results):
        """요약 생성"""
        # 원본 내용 요약
        content_summary = content[:300] + "..." if len(content) > 300 else content
        
        # 분석 개수
        total_analyses = len(analysis_results)
        successful_analyses = sum(1 for r in analysis_results.values() if not r.get('error'))
        
        summary = f"""본 보고서는 제공된 내용을 **10가지 사고 프롬프트**를 통해 다각도로 분석한 결과입니다.

**분석 완료**: {successful_analyses}/{total_analyses}개 관점

**원본 내용 요약**:
{content_summary}

각 관점별 상세 분석은 아래 섹션에서 확인하실 수 있습니다."""
        
        return summary
    
    def _format_analyses(self, analysis_results):
        """분석 결과 포맷팅"""
        formatted = []
        
        for idx, (key, result) in enumerate(analysis_results.items(), 1):
            title = result.get('title', 'Unknown')
            title_en = result.get('title_en', '')
            description = result.get('description', '')
            analysis = result.get('result', '')
            
            section = f"""### {idx}. {title} ({title_en})

**분석 목적**: {description}

**분석 결과**:

{analysis}

---
"""
            formatted.append(section)
        
        return "\n".join(formatted)
    
    def _format_input_type(self, input_type):
        """입력 타입 한글 변환"""
        type_map = {
            'text': '텍스트 직접 입력',
            'url': '웹 페이지 (URL)',
            'pdf': 'PDF 문서'
        }
        return type_map.get(input_type, input_type)
    
    def _truncate_content(self, content, max_length):
        """내용 길이 제한"""
        if len(content) <= max_length:
            return content
        return content[:max_length] + "\n\n... (내용이 길어 일부만 표시됩니다)"
    
    def _sanitize_filename(self, filename):
        """파일명에서 특수문자 제거"""
        import re
        # 특수문자를 언더스코어로 대체
        safe = re.sub(r'[^\w\s-]', '', filename)
        safe = re.sub(r'[-\s]+', '_', safe)
        # 최대 50자로 제한
        return safe[:50]
    
    def _convert_to_pdf(self, md_path, pdf_path):
        """마크다운을 PDF로 변환"""
        import subprocess
        
        try:
            # manus-md-to-pdf 유틸리티 사용
            result = subprocess.run(
                ['manus-md-to-pdf', md_path, pdf_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                raise Exception(f"PDF 변환 실패: {result.stderr}")
            
        except FileNotFoundError:
            # manus-md-to-pdf가 없는 경우 대체 방법 사용
            self._convert_to_pdf_alternative(md_path, pdf_path)
    
    def _convert_to_pdf_alternative(self, md_path, pdf_path):
        """대체 PDF 변환 방법 (WeasyPrint 사용)"""
        from weasyprint import HTML, CSS
        from markdown import markdown
        
        # 마크다운 읽기
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # HTML로 변환
        html_content = markdown(md_content, extensions=['extra', 'codehilite'])
        
        # CSS 스타일 추가
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                body {{
                    font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    border-bottom: 2px solid #95a5a6;
                    padding-bottom: 8px;
                    margin-top: 30px;
                }}
                h3 {{
                    color: #7f8c8d;
                    margin-top: 20px;
                }}
                hr {{
                    border: none;
                    border-top: 1px solid #bdc3c7;
                    margin: 20px 0;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 6px;
                    border-radius: 3px;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                blockquote {{
                    border-left: 4px solid #3498db;
                    padding-left: 15px;
                    color: #555;
                    font-style: italic;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # PDF 생성
        HTML(string=styled_html).write_pdf(pdf_path)


# 테스트 코드
if __name__ == "__main__":
    # 테스트용 더미 데이터
    test_input_data = {
        'content': 'AI 기반 교육 플랫폼 개발 계획입니다. 학습자 맞춤형 콘텐츠를 제공합니다.',
        'metadata': {
            'title': 'AI 교육 플랫폼 계획',
            'source': 'Direct Input',
            'length': 50
        },
        'type': 'text'
    }
    
    test_analysis_results = {
        'challenge_thinking': {
            'title': '내 사고에 도전하기',
            'title_en': 'Challenge my thinking',
            'description': '비판적 사고를 통한 가정과 논리의 검증',
            'result': '이 계획의 주요 가정은 학습자가 AI 추천을 신뢰할 것이라는 점입니다. 그러나 개인정보 보호와 알고리즘 투명성에 대한 우려가 있을 수 있습니다.',
            'timestamp': datetime.now().isoformat()
        }
    }
    
    test_synthesis = """
    종합적으로 볼 때, AI 교육 플랫폼 계획은 혁신적이지만 다음 사항을 고려해야 합니다:
    1. 개인정보 보호 정책 강화
    2. 교육 효과 검증 방법론 구축
    3. 교사와의 협업 모델 개발
    """
    
    generator = ReportGenerator()
    
    print("=== 보고서 생성 테스트 ===\n")
    
    # 마크다운 보고서 생성
    md_path = generator.generate_report(
        test_input_data,
        test_analysis_results,
        test_synthesis,
        output_format='markdown'
    )
    
    print(f"마크다운 보고서 생성 완료: {md_path}")
    
    # 파일 내용 미리보기
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print("\n=== 보고서 내용 미리보기 ===")
        print(content[:500] + "...")

