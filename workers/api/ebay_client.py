import base64
import json
import os
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv()


class EbayApiError(Exception):
    pass


class EbayClient:
    OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"
    SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    SCOPE = "https://api.ebay.com/oauth/api_scope"

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        marketplace_id: str | None = None,
    ):
        self.client_id = client_id or os.getenv("EBAY_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("EBAY_CLIENT_SECRET")
        self.marketplace_id = marketplace_id or os.getenv("EBAY_MARKETPLACE_ID", "EBAY_CA")
        self._access_token = None
        self._access_token_expires_at = 0

        if not self.client_id or not self.client_secret:
            raise EbayApiError("Missing EBAY_CLIENT_ID or EBAY_CLIENT_SECRET")

    def _request_json(self, request: Request):
        try:
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            body = error.read().decode("utf-8")
            raise EbayApiError(f"eBay API error {error.code}: {body}") from error

    def _get_access_token(self):
        if self._access_token and time.time() < self._access_token_expires_at:
            return self._access_token

        credentials = f"{self.client_id}:{self.client_secret}".encode("utf-8")
        encoded_credentials = base64.b64encode(credentials).decode("utf-8")
        body = urlencode({
            "grant_type": "client_credentials",
            "scope": self.SCOPE,
        }).encode("utf-8")

        request = Request(
            self.OAUTH_URL,
            data=body,
            headers={
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )

        payload = self._request_json(request)
        self._access_token = payload["access_token"]
        expires_in = int(payload.get("expires_in", 7200))
        self._access_token_expires_at = time.time() + expires_in - 60

        return self._access_token

    def search(self, query: str, limit: int = 5):
        params = urlencode({
            "q": query,
            "limit": limit,
            "filter": "buyingOptions:{FIXED_PRICE}",
        })
        request = Request(
            f"{self.SEARCH_URL}?{params}",
            headers={
                "Authorization": f"Bearer {self._get_access_token()}",
                "Accept": "application/json",
                "X-EBAY-C-MARKETPLACE-ID": self.marketplace_id,
            },
            method="GET",
        )

        payload = self._request_json(request)
        items = payload.get("itemSummaries", [])
        results = []

        for item in items:
            normalized = self._normalize_item(item, query)

            if normalized:
                results.append(normalized)

        return results

    @staticmethod
    def _normalize_item(item: dict, query: str):
        price = item.get("price") or {}
        price_value = price.get("value")

        if not price_value:
            return None

        return {
            "title": item.get("title"),
            "price": price_value,
            "currency": price.get("currency", "CAD"),
            "source": "ebay",
            "query": query,
            "url": item.get("itemWebUrl"),
            "store_sku": item.get("itemId"),
            "condition": item.get("condition"),
        }
