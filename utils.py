import re
from openai import AsyncOpenAI, OpenAI

OPENAI_API_KEY = ""

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,  
)
sync_client = OpenAI(
    api_key=OPENAI_API_KEY,
)

def llm_call(prompt: str, system_prompt: str = "", model: str = "gpt-4o-mini") -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    chat_completion = sync_client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return chat_completion.choices[0].message.content


async def llm_call_async(prompt: str, system_prompt: str = "", model: str = "gpt-4o-mini") -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    chat_completion = await client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return chat_completion.choices[0].message.content