from langchain_openai import ChatOpenAI
from newsletter.graph.state import WorkflowState
from newsletter.graph.prompts import CREATOR_PROMPT, POST_1, POST_2, POST_3
from pydantic import BaseModel
import json


class _CreatorResponse(BaseModel):
    title: str
    content: str


llm = ChatOpenAI(model="gpt-4o-mini")


def _make_prompt_vars(state: WorkflowState) -> dict:
    original_content = ""

    for i, content in enumerate(state["summary_contents"]):
        original_content += f"ORIGINAL_CONTENT_{i + 1}:\n{content}\n"

    example = f"""
EXAMPLE_1:
{POST_1}

EXAMPLE_2:
{POST_2}
"""

    """
...
EXAMPLE_2:
{POST_2}

EXAMPLE_3:
{POST_3}
"""

    topics = ", ".join(state["topics"])

    return {
        "original_content": original_content,
        "example": example,
        "topics": topics,
    }


def _create_newsletter():
    pass


def creator_node(state: WorkflowState):
    vars = _make_prompt_vars(state)
    prompt = CREATOR_PROMPT.format(**vars)

    response = llm.bind_tools([_CreatorResponse]).invoke(prompt)
    arguments = json.loads(
        response.additional_kwargs["tool_calls"][0]["function"]["arguments"]
    )
    title = arguments.get("title", "")
    content = arguments.get("content", "")
    content += "\n\n참고 자료:\n" + "\n".join(
        f"- {url}" for url in state["search_urls"]
    )
    print("====================creator_node====================")
    print(title)
    print(content)

    state["newsletter_contents"].append(content)
    return {
        "newsletter_title": title,
        "newsletter_content": state["newsletter_contents"],
        "summary_contents": [],
    }
