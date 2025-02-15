from typing import List
from utils import llm_call
from pydantic import BaseModel


# Example 3: Route workflow for customer support ticket handling
# Route support tickets to appropriate teams based on content analysis


def run_router_workflow(user_prompt : str):
    router_prompt = f"""
    사용자의 프롬프트/질문: {user_prompt}

    각 모델은 서로 다른 기능을 가지고 있습니다. 사용자의 질문에 가장 적합한 모델을 선택하세요:
    - gpt-4o: 일반적인 작업에 가장 적합한 모델 (기본값)
    - o1-mini: 코딩 및 복잡한 문제 해결에 적합한 모델
    - gpt-4o-mini: 가벼운 작업이나 보조적인 답변에 적합한 모델
    
    모델명만 단답형으로 응답하세요
    """
    selected_model = llm_call(router_prompt)
    print("선택한 모델", selected_model)
    # Take that route and run the LLM model
    response = llm_call(user_prompt,                   model = selected_model
    )
    print(response)
    return response

# make test cases for example prompt = "주어진 숫자가 소수인지 확인하는 Python 코드 스니펫을 생성하세요."

# test case 1

query3 = "1더하기 2는 뭐지?"
response = run_router_workflow(query3)


query2 = "리스본 여행일정을 짜줘"
response = run_router_workflow(query2)


query1 = "파이썬으로 API 웹서버를 만들어줘"
response = run_router_workflow(query1)




