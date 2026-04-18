from constants import ARTICLE_FILE
from google import genai
from google.genai import types
import os
from pydantic import BaseModel, Field


class ConfigOutput(BaseModel):
    next_paraphrase: str = Field(description="续写出的文段。")
    self_comment: str = Field(description="对写出的文段的自我评价。")


system_prompt = open("prompt.md", encoding="utf8").read()
article_output = open(ARTICLE_FILE, "a+", encoding="utf8")
article_current_content = article_output.read()

ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
chat = ai_client.chats.create(
    model="gemini-2.5-flash",
    history=[
        types.Content(
            parts=[types.Part("我明白了，我会按照你的要求进行续写文段。")],
            role="model",
        ),
    ],
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0),
        system_instruction=system_prompt,
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
response = chat.send_message(article_current_content)

if response.text:
    output = ConfigOutput.model_validate_json(response.text)
    article_output.write(output.next_paraphrase)
    print(output.self_comment)
else:
    print("写不出来")
