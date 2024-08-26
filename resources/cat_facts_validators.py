from typing import List
from .cat_facts_data import Fact


def validate_all_facts_has_not_empty_text(cat_facts_data_lst: List[Fact]) -> None:
    for fact_data in cat_facts_data_lst:
        assert isinstance(fact_data.text, str) and fact_data.text, \
            "Fact text should be a non-empty string"