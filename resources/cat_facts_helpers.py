import json
from typing import List
from .cat_facts_data import Fact


def api_reponse_to_fact_data(api_response) -> List[Fact]:
    fact_datas: List[Fact] = []

    try:
        # Decode the binary content to a string using UTF-8
        response_content = api_response.content.decode('utf-8')

        # Parse the JSON string into a dictionary
        facts_data = json.loads(response_content)

        if isinstance(facts_data, list):
            for fact_data in facts_data:
                fact = Fact.from_dict(fact_data)
                fact_datas.append(fact)
        else:
            fact_datas.append(Fact.from_dict(facts_data))

    except (ValueError, TypeError) as e:
        assert False, f"Failed to convert response to Fact dataclass: {e}"

    return fact_datas