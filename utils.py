import aiohttp
import asyncio
import json
import ollama

OLLAMA_BASE_URL = "http://localhost:11434"

def llm_call(prompt: str, model: str = "mistral") -> str:
    """
    Ollama를 사용하여 동기적으로 모델 호출
    """
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content'] 

async def llm_call_async(prompt: str, model: str = "mistral") -> str:
    """
    Ollama의 API를 비동기적으로 호출하는 함수 (DeprecationWarning 및 NDJSON 대응)
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{OLLAMA_BASE_URL}/api/generate", json={
            "model": model,
            "prompt": prompt
        }) as resp:
            # NDJSON 데이터 처리
            result = ""
            async for line in resp.content:
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))  # JSON 변환
                        if "response" in data:
                            result += data["response"]
                    except json.JSONDecodeError:
                        pass  # 잘못된 JSON 라인은 무시

            print(model, "완료")
            return result

async def main():
    result = await llm_call_async("Hello, Ollama!", "exaone3.5:latest")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())  # ✅ asyncio.run() 사용하여 DeprecationWarning 해결

