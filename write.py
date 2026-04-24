from constants import ARTICLE_FILE, SEED_FILE
from generate import generators
import os
import sys
from structs import ConfigOutput

system_prompt = (
    open("prompt.md", encoding="utf8")
    .read()
    .format(JSON_SCHEMA=ConfigOutput.model_json_schema())
)
if os.path.exists(ARTICLE_FILE):
    print("有article正在续写！！！")
    article_output = open(ARTICLE_FILE, "r+", encoding="utf8")
elif os.path.exists(SEED_FILE):
    print("没有article，正在种下seed！！！！")
    article_output = open(ARTICLE_FILE, "w+", encoding="utf8")
    article_output.write(open(SEED_FILE, encoding="utf8").read())
else:
    print("既没article又没seed")
    sys.exit(1)
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
