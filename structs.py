from pydantic import BaseModel, Field


class ConfigOutput(BaseModel):
    next_paraphrase: str = Field(description="续写出的文段。")
    self_comment: str = Field(description="对写出的文段的自我评价。")
