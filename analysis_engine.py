#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
분석 엔진 (Analysis Engine)
10가지 사고 프롬프트를 활용하여 LLM 기반 다각도 분석 수행
"""

import os
from openai import OpenAI
from datetime import datetime


class ThinkingPromptsEngine:
    """10가지 사고 프롬프트 기반 분석 엔진"""
    
    # 10가지 사고 프롬프트 정의
    PROMPTS = {
        "challenge_thinking": {
            "title": "내 사고에 도전하기",
            "title_en": "Challenge my thinking",
            "description": "비판적 사고를 통한 가정과 논리의 검증",
            "template": """Here's what I'm planning:

{content}

Act as a critical thinker. Question my assumptions, logic, or blind spots — but don't rewrite anything. I want to stress-test my own thinking, not get new ideas.

Please provide your analysis in Korean."""
        },
        "reframe_lens": {
            "title": "다른 렌즈로 재구성하기",
            "title_en": "Reframe through a different lens",
            "description": "새로운 관점에서 아이디어 재해석",
            "template": """Here's the core idea I'm working with:

{content}

Help me reframe it through a different lens — like a new audience POV, emotional trigger, or brand positioning angle.

Please provide your analysis in Korean."""
        },
        "surface_question": {
            "title": "더 깊은 질문 발견하기",
            "title_en": "Surface the deeper question",
            "description": "표면적 문제 뒤에 숨은 본질적 질문 찾기",
            "template": """Here's the situation I'm thinking through:

{content}

Help me uncover the real strategic question underneath this. What should I actually be asking myself?

Please provide your analysis in Korean."""
        },
        "translate_gut_feeling": {
            "title": "직관을 언어화하기",
            "title_en": "Translate my gut feeling",
            "description": "막연한 느낌을 구체적 언어로 전환",
            "template": """Something about this feels off, but I can't explain why:

{content}

Help me put words to the tension I'm sensing. What might be misaligned or unclear?

Please provide your analysis in Korean."""
        },
        "second_order_effects": {
            "title": "2차, 3차 효과 찾기",
            "title_en": "Find the second-order effects",
            "description": "결정의 장기적 파급효과 분석",
            "template": """Here's the decision or idea I'm considering:

{content}

Help me think through the second- and third-order consequences — what might happen after the obvious outcomes?

Please provide your analysis in Korean."""
        },
        "unseen_variable": {
            "title": "보이지 않는 변수 발견하기",
            "title_en": "Reveal the unseen variable",
            "description": "간과된 핵심 변수 식별",
            "template": """Here's the plan or situation I'm analyzing:

{content}

What critical factor might I be overlooking — the hidden variable that could completely change the outcome if noticed?

Please provide your analysis in Korean."""
        },
        "extract_principle": {
            "title": "핵심 원리 추출하기",
            "title_en": "Extract the core principle",
            "description": "성공/실패 사례에서 재사용 가능한 원리 도출",
            "template": """Here's something that worked (or failed):

{content}

Help me extract the underlying principle so I can apply it elsewhere.

Please provide your analysis in Korean."""
        },
        "reverse_engineer_instinct": {
            "title": "직관을 역설계하기",
            "title_en": "Reverse-engineer my instinct",
            "description": "직관적 판단의 논리적 근거 분석",
            "template": """Here's my idea, and it feels right to me:

{content}

Help me unpack why this might make sense — even if I can't fully explain it yet.

Please provide your analysis in Korean."""
        },
        "hidden_pattern": {
            "title": "숨겨진 패턴 찾기",
            "title_en": "Find the hidden pattern",
            "description": "여러 사례를 연결하는 공통 패턴 발견",
            "template": """Here are a few examples or situations I've noticed:

{content}

Help me identify the hidden pattern or principle connecting them.

Please provide your analysis in Korean."""
        },
        "think_in_reverse": {
            "title": "역방향 사고",
            "title_en": "Think in reverse",
            "description": "목표에서 현재로 역추적하여 필요조건 도출",
            "template": """Here's my goal:

{content}

Instead of moving forward, walk me backward from the desired result — what would need to be true at each step for this to succeed?

Please provide your analysis in Korean."""
        }
    }
    
    def __init__(self, model="gpt-4.1-mini"):
        """
        분석 엔진 초기화
        
        Args:
            model: 사용할 OpenAI 모델
        """
        self.client = OpenAI()
        self.model = model
    
    def analyze(self, content, prompts_to_use=None, progress_callback=None):
        """
        10가지 프롬프트를 사용하여 콘텐츠 분석
        
        Args:
            content: 분석할 내용
            prompts_to_use: 사용할 프롬프트 키 리스트 (None이면 전체 사용)
            progress_callback: 진행 상황 콜백 함수
        
        Returns:
            dict: 각 프롬프트별 분석 결과
        """
        if prompts_to_use is None:
            prompts_to_use = list(self.PROMPTS.keys())
        
        results = {}
        total = len(prompts_to_use)
        
        for idx, prompt_key in enumerate(prompts_to_use, 1):
            if prompt_key not in self.PROMPTS:
                continue
            
            prompt_info = self.PROMPTS[prompt_key]
            
            if progress_callback:
                progress_callback(idx, total, prompt_info['title'])
            
            # 프롬프트 생성
            full_prompt = prompt_info['template'].format(content=content)
            
            # LLM 분석 수행
            try:
                analysis_result = self._call_llm(full_prompt)
                
                results[prompt_key] = {
                    'title': prompt_info['title'],
                    'title_en': prompt_info['title_en'],
                    'description': prompt_info['description'],
                    'result': analysis_result,
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                results[prompt_key] = {
                    'title': prompt_info['title'],
                    'title_en': prompt_info['title_en'],
                    'description': prompt_info['description'],
                    'result': f"분석 중 오류 발생: {str(e)}",
                    'error': True,
                    'timestamp': datetime.now().isoformat()
                }
        
        return results
    
    def _call_llm(self, prompt):
        """
        LLM API 호출
        
        Args:
            prompt: 전송할 프롬프트
        
        Returns:
            str: LLM 응답
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a critical thinking assistant that helps analyze ideas, plans, and strategies from multiple perspectives. Provide thoughtful, insightful analysis in Korean."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content.strip()
    
    def get_prompt_info(self, prompt_key):
        """특정 프롬프트 정보 반환"""
        return self.PROMPTS.get(prompt_key)
    
    def get_all_prompts(self):
        """모든 프롬프트 정보 반환"""
        return self.PROMPTS
    
    def generate_summary(self, analysis_results):
        """
        분석 결과를 종합하여 요약 생성
        
        Args:
            analysis_results: analyze() 메서드의 반환값
        
        Returns:
            str: 종합 요약
        """
        # 모든 분석 결과를 하나의 컨텍스트로 결합
        combined_analysis = ""
        for key, result in analysis_results.items():
            if not result.get('error'):
                combined_analysis += f"\n\n## {result['title']}\n{result['result']}"
        
        # 종합 요약 프롬프트
        summary_prompt = f"""다음은 하나의 아이디어/계획/전략을 10가지 관점에서 분석한 결과입니다:

{combined_analysis}

위의 10가지 분석 결과를 종합하여, 다음 내용을 포함한 통합 요약을 작성해주세요:

1. **핵심 인사이트**: 가장 중요한 발견사항 3-5가지
2. **주요 위험 요소**: 반드시 고려해야 할 리스크
3. **개선 방향**: 구체적인 개선 제안
4. **실행 우선순위**: 먼저 해결해야 할 과제

한국어로 작성해주세요."""
        
        try:
            summary = self._call_llm(summary_prompt)
            return summary
        except Exception as e:
            return f"요약 생성 중 오류 발생: {str(e)}"


# 테스트 코드
if __name__ == "__main__":
    # 간단한 테스트
    engine = ThinkingPromptsEngine()
    
    test_content = """
    AI 기반 개인화 학습 플랫폼 개발 계획
    
    우리는 학생들의 학습 패턴을 분석하여 맞춤형 교육 콘텐츠를 제공하는 플랫폼을 개발하려고 합니다.
    주요 기능:
    1. 학습자 수준 자동 진단
    2. AI 기반 콘텐츠 추천
    3. 실시간 학습 피드백
    4. 학습 진도 추적 및 분석
    
    목표 시장: 초중고 학생 및 학부모
    예상 개발 기간: 6개월
    """
    
    print("=== 사고 프롬프트 분석 엔진 테스트 ===\n")
    print("분석 대상:")
    print(test_content)
    print("\n" + "="*50 + "\n")
    
    # 테스트를 위해 첫 2개 프롬프트만 실행
    test_prompts = ["challenge_thinking", "reframe_lens"]
    
    def progress(current, total, title):
        print(f"[{current}/{total}] {title} 분석 중...")
    
    results = engine.analyze(test_content, prompts_to_use=test_prompts, progress_callback=progress)
    
    print("\n" + "="*50 + "\n")
    print("=== 분석 결과 ===\n")
    
    for key, result in results.items():
        print(f"## {result['title']}")
        print(f"{result['description']}\n")
        print(result['result'])
        print("\n" + "-"*50 + "\n")

