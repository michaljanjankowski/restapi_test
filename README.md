# Cat Facts API tests

Integration tests for the public [Cat Facts API](https://catfact.ninja/).

## Run

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and use Python 3.10:

```sh
uv sync --python 3.10
uv run pytest
```

Dependencies are declared in `pyproject.toml` and pinned in `uv.lock`.
The tests send live requests to `https://catfact.ninja` and require internet access.

## Coverage

- `GET /facts`: the response contains a non-empty list of cat facts with valid text and length.
- `GET /fact`: the response contains one random cat fact with valid text and length.
- `POST /facts`: the API returns `404 Not Found` because this endpoint does not support creating facts.
- `GET /facts?limit=3&max_length=100`: the list respects both filters.
- `GET /facts?page=2&limit=3`: pagination returns the requested page.
- `GET /breeds?limit=3`: breed records include their documented fields.
- `POST /mcp` with `tools/list`: the MCP server advertises its cat fact tools.
- `POST /mcp` with `tools/call`: `random-cat-fact` returns a valid fact no longer than 100 characters.

Run only the MCP tests with `uv run pytest test_mcp.py -q`.
