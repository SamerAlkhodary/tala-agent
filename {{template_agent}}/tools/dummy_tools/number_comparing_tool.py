import logging
import os

from contextual_agents_sdk.agents.errors import AgentError, HttpCode
from langchain_core.tools import tool

logger = logging.getLogger(__name__)
github_token = os.environ.get("GITHUB_TOKEN")


@tool
def greater_tool(first_number: float, second_number: float) -> str:
    """
    Compares two numbers and returns the greater one.
    Args:
        first_number: The first number to compare.
        second_number: The second number to compare.
    Returns:
        A dictionary containing the repository URL or an error message.
    """
    try:
        if first_number > second_number:
            return str(first_number)
        else:
            return str(second_number)

    except Exception as e:
        logger.error("Error creating repository: %s", str(e), exc_info=True)
        return AgentError(
            resource_name="greater",
            code=HttpCode.INTERNAL.value,
            message=str(e),
        ).to_json()
