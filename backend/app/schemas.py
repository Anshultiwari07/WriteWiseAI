from typing import Literal
from pydantic import BaseModel


class GenerateRequest(BaseModel):
    topic: str
    format_type: Literal[
        "blog_article",
        "linkedin_post",
        "twitter_thread",
        "instagram_caption",
        "info_paragraph",
        "custom",
    ] = "blog_article"
    length: Literal["short", "medium", "long"] = "medium"
    num_pieces: int = 3
    language: str = "English"


class GenerateResponse(BaseModel):
    plan_markdown: str
    drafts_markdown: str
    final_markdown: str