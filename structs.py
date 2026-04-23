from pydantic import BaseModel, Field


class ConfigOutput(BaseModel):
    next_paraphrase: str = Field(description="续写出的文段。")
    self_comment: str = Field(description="对写出的文段的自我评价。")
    chinese_version: str = Field(
        description="将你续写出的文段（包括用户发送的文段）翻译为中文。"
    )
