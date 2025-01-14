from langchain_openai import ChatOpenAI
from newsletter.graph.state import WorkflowState
from newsletter.graph.prompts import QUERY_OPTIMIZATION_PROMPT
from pydantic import BaseModel
import datetime
import json


llm = ChatOpenAI(model="gpt-4o-mini")


class _OptimizeSearchQuery(BaseModel):
    optimized_search_query: str


def search_optimizer_node(state: WorkflowState):
    topics = ", ".join(state["topics"])
    prompt = QUERY_OPTIMIZATION_PROMPT.format(
        topics=topics,
        current_date=datetime.datetime.now().strftime("%Y-%m-%d"),
    )
    response = llm.bind_tools([_OptimizeSearchQuery]).invoke(prompt)
    arguments = json.loads(
        response.additional_kwargs["tool_calls"][0]["function"]["arguments"]
    )

    optimized_search_query = arguments.get("optimized_search_query", "")
    print("====================search_optimizer====================")
    print(f"Optimized search query: {optimized_search_query}")

    return {"search_queries": [optimized_search_query]}
