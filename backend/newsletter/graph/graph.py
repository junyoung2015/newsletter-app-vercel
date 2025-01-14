from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from newsletter.graph.state import WorkflowState
from newsletter.graph.visualize import save_graph_as_png, display_graph
from newsletter.graph.nodes.search_optimizer import search_optimizer_node
from newsletter.graph.nodes.search import search_node
from newsletter.graph.nodes.summary import summarizer_node
from newsletter.graph.nodes.creator import creator_node


# 워크플로우 구성
def get_graph() -> CompiledStateGraph:
    builder = StateGraph(WorkflowState)

    # 노드 추가
    builder.add_node("search_optimizer", search_optimizer_node)
    builder.add_node("search", search_node)
    builder.add_node("summarizer", summarizer_node)
    builder.add_node("create_newsletter", creator_node)

    # 엣지 추가
    builder.add_edge(START, "search_optimizer")
    builder.add_edge("search_optimizer", "search")
    builder.add_edge("search", "summarizer")
    builder.add_edge("summarizer", "create_newsletter")
    builder.add_edge("create_newsletter", END)

    graph = builder.compile()

    # 그래프 시각화
    save_graph_as_png(graph, "workflow.png")
    # display_graph(graph)

    return graph
