import requests

from resources.cat_facts_data import ApiError, BreedsPage, BreedsQuery, Fact, FactsPage, FactsQuery
from resources.cat_facts_validators import validate_all_facts_have_non_empty_text


CAT_FACTS_API = "https://catfact.ninja"
TIMEOUT = 10


def test_get_facts():
    response = requests.get(f"{CAT_FACTS_API}/facts", timeout=TIMEOUT)

    assert response.status_code == 200
    page = FactsPage.from_dict(response.json())
    assert page.data, "Expected at least one cat fact"
    validate_all_facts_have_non_empty_text(page.data)


def test_post_facts_is_not_available():
    response = requests.post(f"{CAT_FACTS_API}/facts", timeout=TIMEOUT)

    assert response.status_code == 404
    error = ApiError.from_dict(response.json())
    assert error.message == "Not Found"


def test_get_random_fact():
    response = requests.get(f"{CAT_FACTS_API}/fact", timeout=TIMEOUT)

    assert response.status_code == 200
    fact = Fact.from_dict(response.json())
    validate_all_facts_have_non_empty_text([fact])


def test_get_facts_respects_limit_and_max_length():
    response = requests.get(
        f"{CAT_FACTS_API}/facts",
        params=FactsQuery(limit=3, max_length=100).to_params(),
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    page = FactsPage.from_dict(response.json())
    assert len(page.data) == 3
    validate_all_facts_have_non_empty_text(page.data)
    assert all(fact.length <= 100 for fact in page.data)


def test_get_facts_second_page():
    response = requests.get(
        f"{CAT_FACTS_API}/facts",
        params=FactsQuery(page=2, limit=3).to_params(),
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    page = FactsPage.from_dict(response.json())
    assert page.current_page == 2
    assert len(page.data) == 3
    validate_all_facts_have_non_empty_text(page.data)


def test_get_breeds_with_limit():
    response = requests.get(
        f"{CAT_FACTS_API}/breeds",
        params=BreedsQuery(limit=3).to_params(),
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    page = BreedsPage.from_dict(response.json())
    assert len(page.data) == 3
    for breed in page.data:
        for value in (breed.breed, breed.country, breed.origin, breed.coat, breed.pattern):
            assert isinstance(value, str) and value.strip()
