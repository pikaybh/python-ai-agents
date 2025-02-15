import asyncio

from utils import llm_call_async

async def run_llm_parallel(prompt_details):
    """
    여러 개의 LLM API 호출을 병렬로 실행하고 응답을 수집합니다.

    Args:
        prompts (list): 모델에 보낼 프롬프트 목록.
        system_prompt (str, optional): 모든 호출에 적용될 공통 시스템 프롬프트. 기본값은 "".
        model (str, optional): 사용할 모델. 기본값은 "gpt-4o-mini".

    Returns:
        list: 모델 응답 목록.
    """
    tasks = [llm_call_async(prompt['user_prompt'], prompt['model']) for prompt in prompt_details]
    responses = []
    
    for task in asyncio.as_completed(tasks):
        result = await task
        print("LLM 응답 완료:", result)
        responses.append(result)
    
    return responses

async def main():

    question = """아래 문장을 자연스러운 한국어로 번역해줘:
"Do what you can, with what you have, where you are."— Theodore Roosevelt
"""
    parallel_prompt_details = [
        {
            "user_prompt": question, 
            "model": "gpt-4o"
        },
        {
            "user_prompt": question, 
            "model": "gpt-4o-mini"
        },
        {
            "user_prompt": question, 
            "model": "o1-mini"
        },

    ]

    responses = await run_llm_parallel(parallel_prompt_details)

    aggregator_system_prompt = """다음은 여러 개의 오픈 소스 모델이 사용자 질문에 대해 생성한 응답입니다.
    당신의 역할은 이 응답들을 종합하여 하나의 고품질 답변을 생성하는 것입니다. 
    일부 응답이 부정확하거나 편향될 수 있음을 인식하고, 단순한 복사가 아니라 정제되고 정확한 답변을 제공하세요.
    최상의 신뢰성과 정확성을 갖춘 응답을 생성하는 것이 중요합니다.

    모델 응답들:"""

    aggregated_prompt = aggregator_system_prompt + "\n" + "\n".join(f"{i+1}. {response}" for i, response in enumerate(responses))

    print   ("---------------------------종합 프롬프트:-----------------------\n", aggregated_prompt)
    final_response = await llm_call_async(aggregated_prompt, model="gpt-4o")
    print("---------------------------최종 종합 응답:-----------------------\n", final_response)

# 비동기 main 함수 실행
asyncio.run(main())
