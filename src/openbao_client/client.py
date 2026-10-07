from typing import Any

import requests


class OpenBaoError(Exception):
    """Base exception for OpenBao client errors."""


class OpenBaoClient:
    def __init__(
        self,
        address: str,
        token: str,
        timeout: float = 10.0,
    ):
        self.address = address.rstrip("/")
        self.token = token
        self.timeout = timeout

    def get_secret(self, path: str) -> dict[str, Any]:
        response = self._request(
            "GET",
            f"/v1/secret/data/{path}",
        )

        return response["data"]["data"]

    def put_secret(
        self,
        path: str,
        data: dict[str, Any],
    ) -> None:
        self._request(
            "POST",
            f"/v1/secret/data/{path}",
            json={"data": data},
        )

    def delete_secret(self, path: str) -> None:
        self._request(
            "DELETE",
            f"/v1/secret/data/{path}",
        )

    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        try:
            response = requests.request(
                method,
                f"{self.address}{path}",
                headers={
                    "X-Vault-Token": self.token,
                },
                timeout=self.timeout,
                **kwargs,
            )
        except requests.RequestException as exc:
            raise OpenBaoError(
                f"Failed to connect to OpenBao: {exc}"
            ) from exc

        if not response.ok:
            raise OpenBaoError(
                f"OpenBao request failed "
                f"({response.status_code}): {response.text}"
            )

        if not response.content:
            return {}

        return response.json()