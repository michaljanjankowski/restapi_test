import requests
import json
from resources.cat_facts_helpers import api_reponse_to_fact_data
from resources.cat_facts_validators import validate_all_facts_has_not_empty_text

CAT_FACTS_ENDPOINT = "cat-fact.herokuapp.com"


def test_positice_get_facts():
    # Step 1: Send GET request to `/facts`
    response = requests.get(f"https://{CAT_FACTS_ENDPOINT}/facts")

    # Step 2: Validate response status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Step 3: Convert response to Fact dataclass and validate fields types
    fact_datas = api_reponse_to_fact_data(api_response=response)

    # Step 4: Validate the `text` field
    if fact_datas:
        validate_all_facts_has_not_empty_text(cat_facts_data_lst=fact_datas)



def test_negative_try_post_fact():
    # Step 1: Send POST request to `/facts`
    response = requests.post(f"https://{CAT_FACTS_ENDPOINT}/facts")
    # Step 2: Verify status code is 401
    assert response.status_code == 401
    text_json = json.loads(response.text)
    # Step 3: Verify error message content
    assert text_json['message'] == "Sign in first"


def test_positice_get_facts_random():
    # Step 1: Send GET request to `/facts`
    response = requests.get(f"https://{CAT_FACTS_ENDPOINT}/facts/random")

    # Step 2: Validate response status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Step 3: Convert response to Fact dataclass and validate fields types
    fact_datas = api_reponse_to_fact_data(api_response=response)

    # Step 4: Validate the `text` field
    if fact_datas:
        validate_all_facts_has_not_empty_text(cat_facts_data_lst=fact_datas)