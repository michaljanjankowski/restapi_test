import json
from dataclasses import asdict, dataclass
from typing import List, Optional, Union

from .cat_facts_data import Fact


@dataclass
class ListToolsParams:
    pass


@dataclass
class RandomFactArguments:
    max_length: int


@dataclass
class CallToolParams:
    name: str
    arguments: RandomFactArguments


@dataclass
class McpRequest:
    id: int
    method: str
    params: Union[ListToolsParams, CallToolParams]
    jsonrpc: str = "2.0"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class McpTool:
    name: str


@dataclass
class ListToolsResult:
    tools: List[McpTool]

    @classmethod
    def from_dict(cls, data: dict) -> "ListToolsResult":
        return cls(tools=[McpTool(name=tool["name"]) for tool in data["tools"]])


@dataclass
class McpContent:
    type: str
    text: Optional[str] = None

    def as_fact(self) -> Fact:
        assert self.type == "text" and self.text is not None
        return Fact.from_dict(json.loads(self.text))


@dataclass
class CallToolResult:
    content: List[McpContent]
    is_error: bool

    @classmethod
    def from_dict(cls, data: dict) -> "CallToolResult":
        return cls(
            content=[McpContent(type=item["type"], text=item.get("text")) for item in data["content"]],
            is_error=data["isError"],
        )


@dataclass
class McpResponse:
    id: int
    result: Union[ListToolsResult, CallToolResult]
    jsonrpc: str = "2.0"

    @classmethod
    def from_dict(cls, data: dict, method: str) -> "McpResponse":
        assert data["jsonrpc"] == "2.0"
        assert "error" not in data, data.get("error")
        result_type = ListToolsResult if method == "tools/list" else CallToolResult
        return cls(id=data["id"], result=result_type.from_dict(data["result"]))
