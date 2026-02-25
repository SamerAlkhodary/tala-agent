import json
from unittest.mock import patch

import pytest
from {{template_agent}}.tools import greater_tool


@pytest.fixture
def mock_dependencies():
    with patch("{{template_agent}}.tools.dummy_tools.number_comparing_tool.logger") as mock_logger:
        yield {
            "logger": mock_logger,
        }


@pytest.mark.asyncio
async def test_greater_tool_returns_first_number_when_greater():
    """Test that the tool returns the first number when it is greater."""
    result = await greater_tool.ainvoke(
        {
            "type": "tool_call",
            "name": "greater_tool",
            "id": "test-tool-call-id",
            "args": {
                "first_number": 10.0,
                "second_number": 5.0,
            },
        }
    )

    assert result.content == "10.0"


@pytest.mark.asyncio
async def test_greater_tool_returns_second_number_when_greater():
    """Test that the tool returns the second number when it is greater."""
    result = await greater_tool.ainvoke(
        {
            "type": "tool_call",
            "name": "greater_tool",
            "id": "test-tool-call-id",
            "args": {
                "first_number": 3.0,
                "second_number": 7.0,
            },
        }
    )

    assert result.content == "7.0"


@pytest.mark.asyncio
async def test_greater_tool_returns_second_number_when_equal():
    """Test that the tool returns the second number when both are equal."""
    result = await greater_tool.ainvoke(
        {
            "type": "tool_call",
            "name": "greater_tool",
            "id": "test-tool-call-id",
            "args": {
                "first_number": 5.0,
                "second_number": 5.0,
            },
        }
    )

    assert result.content == "5.0"


@pytest.mark.asyncio
async def test_greater_tool_with_negative_numbers():
    """Test that the tool works correctly with negative numbers."""
    result = await greater_tool.ainvoke(
        {
            "type": "tool_call",
            "name": "greater_tool",
            "id": "test-tool-call-id",
            "args": {
                "first_number": -3.0,
                "second_number": -7.0,
            },
        }
    )

    assert result.content == "-3.0"


@pytest.mark.asyncio
async def test_greater_tool_with_decimal_numbers():
    """Test that the tool works correctly with decimal numbers."""
    result = await greater_tool.ainvoke(
        {
            "type": "tool_call",
            "name": "greater_tool",
            "id": "test-tool-call-id",
            "args": {
                "first_number": 3.14159,
                "second_number": 2.71828,
            },
        }
    )

    assert result.content == "3.14159"


@pytest.mark.asyncio
async def test_greater_tool_with_zero_values():
    """Test that the tool works correctly with zero values."""
    result = await greater_tool.ainvoke(
        {
            "type": "tool_call",
            "name": "greater_tool",
            "id": "test-tool-call-id",
            "args": {
                "first_number": 0.0,
                "second_number": -1.0,
            },
        }
    )

    assert result.content == "0.0"


@pytest.mark.asyncio
async def test_greater_tool_with_large_numbers():
    """Test that the tool works correctly with large numbers."""
    result = await greater_tool.ainvoke(
        {
            "type": "tool_call",
            "name": "greater_tool",
            "id": "test-tool-call-id",
            "args": {
                "first_number": 1000000.0,
                "second_number": 999999.0,
            },
        }
    )

    assert result.content == "1000000.0"


def test_greater_tool_name():
    """Test that the tool has the correct name."""
    assert greater_tool.name == "greater_tool"


def test_greater_tool_description():
    """Test that the tool has a description."""
    assert greater_tool.description is not None
    assert len(greater_tool.description) > 0


def test_greater_tool_has_args_schema():
    """Test that the tool has proper args schema for agent integration."""
    assert greater_tool.args_schema is not None
