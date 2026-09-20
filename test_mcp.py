import json

import requests

from resources.cat_facts_data import Fact
from resources.cat_facts_validators import validate_all_facts_have_non_empty_text


MCP_ENDPOINT = "https://catfact.ninja/mcp"
HEADERS = {"Accept": "application/json, text/event-stream"}
TIMEOUT = 10


def call_mcp(request_id, method, params):
    response = requests.post(
        MCP_ENDPOINT,
        headers=HEADERS,
        json={"jsonrpc": "2.0", "id": request_id, "method": method, "params": params},
        timeout=TIMEOUT,
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["jsonrpc"] == "2.0"
    assert payload["id"] == request_id
    assert "error" not in payload
    return payload["result"]


def test_mcp_lists_cat_fact_tools():
    result = call_mcp(1, "tools/list", {})

    names = {tool["name"] for tool in result["tools"]}
    assert {"random-cat-fact", "list-cat-facts", "list-breeds"} <= names


def test_mcp_calls_random_cat_fact():
    result = call_mcp(
        2,
        "tools/call",
        {"name": "random-cat-fact", "arguments": {"max_length": 100}},
    )

    assert result["isError"] is False
    text_items = [item["text"] for item in result["content"] if item["type"] == "text"]
    assert len(text_items) == 1
    fact = Fact.from_dict(json.loads(text_items[0]))
    validate_all_facts_have_non_empty_text([fact])
    assert fact.length <= 100
