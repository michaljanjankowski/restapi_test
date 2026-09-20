import requests

from resources.cat_facts_helpers import api_response_to_fact_data
from resources.cat_facts_validators import validate_all_facts_have_non_empty_text


CAT_FACTS_API = "https://catfact.ninja"
TIMEOUT = 10


def test_get_facts():
    response = requests.get(f"{CAT_FACTS_API}/facts", timeout=TIMEOUT)

    assert response.status_code == 200
    facts = api_response_to_fact_data(response)
    assert facts, "Expected at least one cat fact"
    validate_all_facts_have_non_empty_text(facts)


def test_post_facts_is_not_available():
    response = requests.post(f"{CAT_FACTS_API}/facts", timeout=TIMEOUT)

    assert response.status_code == 404
    assert response.json()["message"] == "Not Found"


def test_get_random_fact():
    response = requests.get(f"{CAT_FACTS_API}/fact", timeout=TIMEOUT)

    assert response.status_code == 200
    facts = api_response_to_fact_data(response)
    assert len(facts) == 1
    validate_all_facts_have_non_empty_text(facts)


def test_get_facts_respects_limit_and_max_length():
    response = requests.get(
        f"{CAT_FACTS_API}/facts",
        params={"limit": 3, "max_length": 100},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    facts = api_response_to_fact_data(response)
    assert len(facts) == 3
    validate_all_facts_have_non_empty_text(facts)
    assert all(fact.length <= 100 for fact in facts)


def test_get_facts_second_page():
    response = requests.get(
        f"{CAT_FACTS_API}/facts", params={"page": 2, "limit": 3}, timeout=TIMEOUT
    )

    assert response.status_code == 200
    assert response.json()["current_page"] == 2
    facts = api_response_to_fact_data(response)
    assert len(facts) == 3
    validate_all_facts_have_non_empty_text(facts)


def test_get_breeds_with_limit():
    response = requests.get(
        f"{CAT_FACTS_API}/breeds", params={"limit": 3}, timeout=TIMEOUT
    )

    assert response.status_code == 200
    breeds = response.json()["data"]
    assert len(breeds) == 3
    for breed in breeds:
        for field in ("breed", "country", "origin", "coat", "pattern"):
            assert isinstance(breed[field], str) and breed[field].strip()
