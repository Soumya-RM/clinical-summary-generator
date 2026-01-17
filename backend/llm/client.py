import os
import json
import re
from groq import Groq
from backend.llm.prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from backend.llm.utils import make_json_safe

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_json(text: str) -> dict:
    """
    Extract first JSON object from LLM output safely.
    """
    if not text:
        raise ValueError("Empty response from LLM")

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in LLM response:\n{text}")

    return json.loads(match.group())

def generate_summary(context: dict) -> dict:
    safe_context = make_json_safe(context)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(
                    context=json.dumps(safe_context, indent=2)
                )
            }
        ],
        temperature=0.2
    )

    raw_content = response.choices[0].message.content

    # DEBUG VISIBILITY
    print("\n--- RAW LLM OUTPUT ---\n")
    print(raw_content)
    print("\n--- END RAW OUTPUT ---\n")

    return extract_json(raw_content)
