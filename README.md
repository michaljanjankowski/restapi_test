# RestAPI tests for cat-fact.herokuapp.com

## Tests descriptions

- [Test_GET_facts](#get-facts)
- [Test_POST_facts](#post-facts-negativ)
- [Test_GAT_facts_random](#get-facts-random)

## Get Facts
| Steps | Action                   | Expected result       |
|-------|--------------------------|-----------------------|
| 1     | Send GET /facts          | GET send succesfully  |
| 2     | Validate response status | Response status shall be 200|
|3 | Validate response content stucture| Response strocture shall be like in API specification
|4| Validate facts feature | Each fact shall contain not empty text, feature verification|

## Post Facts Negativ
| Steps | Action                         | Expected result                                                                                           |
|-------|--------------------------------|-----------------------------------------------------------------------------------------------------------|
| 1     | Send POST /facts               | POST send succesfully                                                                                     |
| 2     | Validate response status       | Response status shall be 401, beacuase I am not autheticatied user. Authetication is possible only via UI |
|3 | Validate error message content | Error message shall contain "Sign in first"                                                                |

## Get Facts Random
| Steps | Action                             | Expected result       |
|-------|------------------------------------|-----------------------|
| 1     | Send GET /facts/random             | GET send succesfully  |
| 2     | Validate response status           | Response status shall be 200|
|3 | Validate response content stucture | Response strocture shall be like in API specification
|4| Validate facts feature             | Each fact shall contain not empty text, feature verification|


**Test designs comments:**
- Test basis are taken from cat-facts API specification,
- Firts and third tests are positive tests, that verifies endpoints functions and the content of delivered responses to GET calls,
- Second test is negative security test, that verifies if not autheticated user can not add a fact. 
  - It bases on current cat-facts implemtation, that user authetication can be done only via UI.