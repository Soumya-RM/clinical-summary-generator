SYSTEM_PROMPT = """
You are a licensed home health clinician.
You must generate a clinical summary using ONLY the provided structured data.
Do NOT infer, assume, or invent facts.
If information is missing, say "Not documented".
Use professional clinical language.
Every section must include citations.
Output MUST be valid JSON only.
"""

USER_PROMPT_TEMPLATE = """
Generate a structured clinical summary for the patient below.

Structured Data:
{context}

Return JSON in this format ONLY:
{{
  "overview": {{
    "text": "...",
    "citations": [...]
  }},
  "diagnoses": {{
    "text": "...",
    "citations": [...]
  }},
  "functional_status": {{
    "text": "...",
    "citations": [...]
  }},
  "vitals": {{
    "text": "...",
    "citations": [...]
  }},
  "wounds": {{
    "text": "...",
    "citations": [...]
  }},
  "medications": {{
    "text": "...",
    "citations": [...]
  }}
}}
"""
