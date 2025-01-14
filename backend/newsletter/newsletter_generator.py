from newsletter.graph.graph import get_graph
from newsletter.graph.state import WorkflowState, initialize_state


# Function to call API
def create_newsletter(topics: list[str], sources: list[str]) -> dict:
    graph = get_graph()
    state = WorkflowState(initialize_state(topics=topics, sources=sources))
    res = graph.invoke(state, {"recursion_limit": 100})

    res_dict = {
        "title": res["newsletter_title"],
        "content": res["newsletter_contents"][-1],
    }
    return res_dict


import sys
import os
from newsletter.graph.parse import get_unique_filename

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python newsletter.py <topic> [source]")
        sys.exit(1)

    topic = sys.argv[1]
    source = ""
    if len(sys.argv) > 2:
        source = sys.argv[2]

    res = create_newsletter([topic], [source])

    print("--------------------------------------")
    print(res["title"])
    print(res["content"])
    current_directory = os.getcwd()
    filename = get_unique_filename(f"{current_directory}/output", "newsletter")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(res["title"])
        f.write(res["content"])
