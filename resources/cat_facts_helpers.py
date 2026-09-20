from typing import List

from .cat_facts_data import Fact


def api_response_to_fact_data(api_response) -> List[Fact]:
    payload = api_response.json()
    if "data" in payload:
        assert isinstance(payload["data"], list), "Expected a list of facts"
        return [Fact.from_dict(item) for item in payload["data"]]
    return [Fact.from_dict(payload)]
