from constants import ARTICLE_FILE
from generate import generators
import os
import sys
from structs import ConfigOutput

system_prompt = (
    open("prompt.md", encoding="utf8")
    .read()
    .format(JSON_SCHEMA=ConfigOutput.model_json_schema())
)
article_output = open(ARTICLE_FILE, "r+", encoding="utf8")
article_current_content = article_output.read()
apikey = os.environ.get("AI_APIKEY")
generator_id = os.environ.get("AI_GENERATOR")

if not (generator_id and apikey):
    print("没写配置")
    sys.exit(1)
generate = generators[generator_id]
if not generate:
    print("生成器不对")
    sys.exit(1)
print("当前文段：", article_current_content)
text = generate(article_current_content, system_prompt, apikey)
if not text:
    print("写不出来")
    sys.exit(1)
response = ConfigOutput.model_validate_json(text)
print("续写：", response.next_paraphrase)
print("自评：", response.self_comment)
print("中文全文：", response.chinese_version)
article_output.write(f"\n{response.next_paraphrase}")
