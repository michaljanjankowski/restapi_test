from typing import List

from .cat_facts_data import Fact


def validate_all_facts_have_non_empty_text(facts: List[Fact]) -> None:
    for fact in facts:
        assert fact.fact.strip(), "Fact text should be non-empty"
        assert fact.length == len(fact.fact), "Fact length should match text length"
