from typing_extensions import TypedDict


class WorkflowState(TypedDict):
    search_queries: list[str]  # Search terms related to the newsletter
    search_urls: list[str]  # URLs related to the search results
    search_results: list[str]  # Search results related to the newsletter content
    summary_contents: list[str]  # Translated and summarized content
    newsletter_title: str  # Title of the newsletter
    newsletter_contents: list[str]  # The main content of the newsletter
    topics: list[str]  # Topics related to the newsletter
    sources: list[str]  # Sources related to the newsletter


def initialize_state(**kwargs) -> WorkflowState:
    """
    Initialize the workflow state for the newsletter generation process.
    Args:
        search_query (str): The initial search term related to the newsletter.
        **kwargs: Additional keyword arguments to override the default state values.
    Returns:
        WorkflowState: A dictionary representing the initial state of the workflow.
    WorkflowState Structure:
        intent_of_requested_content (str): Intent of the requested content.
        search_queries (list[str]): Search terms related to the newsletter.
        search_urls (list[str]): URLs related to the search results.
        search_results (list[str]): Search results related to the newsletter content.
        summary_contents (list[str]): Translated and summarized content.
        newsletter_contents (list[str]): The main content of the newsletter.
        is_approved (bool): Approval status of the newsletter.
        remaining_loops (int): Remaining loops for the workflow.
    """

    state: WorkflowState = {
        "search_queries": [],
        "search_urls": [],
        "search_results": [],
        "summary_contents": [],
        "newsletter_title": "",
        "newsletter_contents": [],
        "topics": [],
        "sources": [],
    }

    for key, value in kwargs.items():
        if key in state:
            state[key] = value

    return state
