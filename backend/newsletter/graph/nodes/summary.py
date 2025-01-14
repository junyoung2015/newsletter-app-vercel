from langchain_openai import ChatOpenAI
from newsletter.graph.state import WorkflowState
from newsletter.graph.prompts import SUMMARIZER_PROMPT
from pydantic import BaseModel
import json


llm = ChatOpenAI(model="gpt-4o-mini")


class _SummarizerResponse(BaseModel):
    is_related: bool
    summary: str


def _summarize_content(summary_dict: dict):
    prompt = SUMMARIZER_PROMPT.format(**summary_dict)

    response = llm.bind_tools([_SummarizerResponse]).invoke(prompt)
    arguments = json.loads(
        response.additional_kwargs["tool_calls"][0]["function"]["arguments"]
    )
    is_related = arguments.get("is_related", False)
    summary = arguments.get("summary", "")
    if is_related:
        return summary
    else:
        return ""


def summarizer_node(state: WorkflowState):
    topics = ", ".join(state["topics"])
    new_summary_contents = state["summary_contents"]
    summary_dict = {
        "original_content": "",
        "topics": topics,
    }

    while len(state["search_results"]) > 0:
        summary_dict["original_content"] = state["search_results"].pop(0)
        if len(summary_dict["original_content"]) > 5000:
            summary_content = _summarize_content(summary_dict)
        else:
            summary_content = summary_dict["original_content"]
        if summary_content:
            new_summary_contents.append(summary_content)

    print("====================summarizer_node====================")
    for idx, content in enumerate(new_summary_contents):
        print(
            f"search_results[{idx}]:"
            f" {content[:100] + '...' if len(content) > 100 else content}"
        )

    return {"summary_contents": new_summary_contents}
