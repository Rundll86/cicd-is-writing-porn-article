from constants import ARTICLE_FILE
from generate import generators
import os
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

if generator_id and apikey:
    generate = generators[generator_id]
    if generate:
        print("当前文段：", article_current_content)
        text = generate(article_current_content, system_prompt, apikey)
        if text:
            response = ConfigOutput.model_validate_json(text)
            print("续写：", response.next_paraphrase)
            print("自评：", response.self_comment)
            article_output.write(f"\n{response.next_paraphrase}")
        else:
            print("写不出来")
    else:
        print("生成器不对")
else:
    print("没写配置")
