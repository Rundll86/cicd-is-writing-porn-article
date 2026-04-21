from openai import OpenAI
from constants import AI_RESPONSEOK
from google import genai
from google.genai import types

from structs import ConfigOutput


#
def generate_rotafans(current: str, prompt: str, apikey: str) -> str | None:
    return (
        OpenAI(
            api_key=apikey,
            base_url="https://api.hujiarong.site/v1",
        )
        .chat.completions.create(
            model="grok-4.20-fast",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "assistant", "content": AI_RESPONSEOK},
                {"role": "user", "content": current},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "output",
                    "strict": True,
                    "schema": ConfigOutput.model_json_schema(),
                },
            },
            stream=False,
        )
        .choices[0]
        .message.content
    )


def generate_gemini(current: str, prompt: str, apikey: str) -> str | None:
    return (
        genai.Client(api_key=apikey)
        .chats.create(
            model="gemini-2.5-flash",
            history=[
                types.Content(parts=[types.Part(AI_RESPONSEOK)], role="model"),
            ],
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0),
                system_instruction=prompt,
                safety_settings=[
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    ),
                ],
                response_json_schema=ConfigOutput.model_json_schema(),
                response_mime_type="application/json",
            ),
        )
        .send_message(current)
        .text
    )


generators = {
    "rotafans": generate_rotafans,
    "gemini": generate_gemini,
}
