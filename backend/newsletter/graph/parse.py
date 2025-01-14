import os
import re


def get_unique_filename(directory, base_filename, extension="md"):
    """
    Returns a unique filename by appending a counter to the base filename if a file with the same name already exists.

    Args:
        directory (str): The directory where the file will be saved.
        base_filename (str): The base name of the file without extension.
        extension (str, optional): The file extension. Defaults to ".md".

    Returns:
        str: A unique file path with the given base filename and extension.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not directory.endswith("/"):
        directory += "/"
    file_path = os.path.join(directory, f"{base_filename}.{extension}")
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(directory, f"{base_filename}_{counter}.{extension}")
        counter += 1
    return file_path


def parse(response):
    """
    Parses the response to extract AI messages, tool message URLs and contents, and tool message artifact results.

    Args:
        response (dict): The response dictionary containing messages.

    Returns:
        tuple: A tuple containing three lists:
            - ai_message_contents (list): List of AI message contents.
            - tool_message_urls_and_contents (list): List of dictionaries with URLs and contents from tool messages.
            - tool_message_artifact_results (list): List of dictionaries with artifact results from tool messages.
    """
    ai_message_contents = []
    tool_message_urls_and_contents = []
    tool_message_artifact_results = []
    # Loop through each message in the "messages" list
    for message in response["messages"]:
        # Check if it's an AIMessage and extract its content
        if message.__class__.__name__ == "AIMessage":
            content = getattr(message, "content", "")
            if content:
                ai_message_contents.append(content)

        # Check if it's a ToolMessage and extract its content
        if message.__class__.__name__ == "ToolMessage":
            content = getattr(message, "content", "")

            # Extract URLs and contents from the ToolMessage content using regex
            matches = re.findall(r'{"url": "(.*?)", "content": "(.*?)"}', content)
            for match in matches:
                url, content = match
                tool_message_urls_and_contents.append({"url": url, "content": content})

            # Extract information from the ToolMessage's artifact results
            artifact = getattr(message, "artifact", {})
            results = (
                artifact.get("results", [])
                if isinstance(artifact, dict)
                else getattr(artifact, "results", [])
            )
            for result in results:
                title = (
                    result.get("title", "")
                    if isinstance(result, dict)
                    else getattr(result, "title", "")
                )
                url = (
                    result.get("url", "")
                    if isinstance(result, dict)
                    else getattr(result, "url", "")
                )
                content = (
                    result.get("content", "")
                    if isinstance(result, dict)
                    else getattr(result, "content", "")
                )
                tool_message_artifact_results.append(
                    {"title": title, "url": url, "content": content}
                )
    return (
        ai_message_contents,
        tool_message_urls_and_contents,
        tool_message_artifact_results,
    )
