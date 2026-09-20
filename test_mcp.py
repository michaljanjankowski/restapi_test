import requests

from resources.cat_facts_validators import validate_all_facts_have_non_empty_text
from resources.mcp_data import (
    CallToolParams,
    CallToolResult,
    ListToolsParams,
    ListToolsResult,
    McpRequest,
    McpResponse,
    RandomFactArguments,
)


MCP_ENDPOINT = "https://catfact.ninja/mcp"
HEADERS = {"Accept": "application/json, text/event-stream"}
TIMEOUT = 10


def call_mcp(request: McpRequest) -> McpResponse:
    response = requests.post(
        MCP_ENDPOINT,
        headers=HEADERS,
        json=request.to_dict(),
        timeout=TIMEOUT,
    )
    assert response.status_code == 200
    result = McpResponse.from_dict(response.json(), request.method)
    assert result.id == request.id
    return result


def test_mcp_lists_cat_fact_tools():
    response = call_mcp(McpRequest(id=1, method="tools/list", params=ListToolsParams()))

    assert isinstance(response.result, ListToolsResult)
    names = {tool.name for tool in response.result.tools}
    assert {"random-cat-fact", "list-cat-facts", "list-breeds"} <= names


def test_mcp_calls_random_cat_fact():
    response = call_mcp(
        McpRequest(
            id=2,
            method="tools/call",
            params=CallToolParams(
                name="random-cat-fact", arguments=RandomFactArguments(max_length=100)
            ),
        )
    )

    assert isinstance(response.result, CallToolResult)
    assert response.result.is_error is False
    text_items = [item for item in response.result.content if item.type == "text"]
    assert len(text_items) == 1
    fact = text_items[0].as_fact()
    validate_all_facts_have_non_empty_text([fact])
    assert fact.length <= 100
