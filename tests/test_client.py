import responses

from openbao_client import OpenBaoClient, OpenBaoError


@responses.activate
def test_get_secret():
    responses.add(
        responses.GET,
        "http://openbao:8200/v1/secret/data/data_ingest",
        json={
            "data": {
                "data": {
                    "api_key": "test-api-key",
                }
            }
        },
        status=200,
    )

    client = OpenBaoClient(
        address="http://openbao:8200",
        token="test-token",
    )

    result = client.get_secret("data_ingest")

    assert result == {
        "api_key": "test-api-key",
    }


@responses.activate
def test_put_secret():
    responses.add(
        responses.POST,
        "http://openbao:8200/v1/secret/data/data_ingest",
        json={},
        status=200,
    )

    client = OpenBaoClient(
        address="http://openbao:8200",
        token="test-token",
    )

    client.put_secret(
        "data_ingest",
        {"api_key": "new-key"},
    )

    assert responses.calls[0].request.headers["X-Vault-Token"] == "test-token"


@responses.activate
def test_permission_error():
    responses.add(
        responses.GET,
        "http://openbao:8200/v1/secret/data/data_ingest",
        body='{"errors":["permission denied"]}',
        status=403,
    )

    client = OpenBaoClient(
        address="http://openbao:8200",
        token="test-token",
    )

    try:
        client.get_secret("data_ingest")
        assert False, "Expected OpenBaoError"
    except OpenBaoError as exc:
        assert "403" in str(exc)
