import os
import unittest
from urllib.error import HTTPError
from unittest.mock import Mock, patch

from models import AssetQuote
from providers import BrapiProvider, DataProvider, FallbackDataProvider


class StaticProvider(DataProvider):
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error

    def get_asset_quote(self, ticker: str) -> AssetQuote:
        if self.error:
            raise self.error
        return self.result


class FallbackDataProviderTests(unittest.TestCase):
    def test_falls_back_when_primary_provider_fails(self):
        quote = AssetQuote("PETR4.SA", "Petrobras", 36.5, "BRL", 36.0, source="Brapi")
        provider = FallbackDataProvider(
            [StaticProvider(error=ValueError("indisponível")), StaticProvider(result=quote)]
        )

        self.assertIs(provider.get_asset_quote("PETR4.SA"), quote)

    def test_falls_back_when_primary_provider_has_no_valid_price(self):
        invalid_quote = AssetQuote("PETR4.SA", "Petrobras", 0, "BRL", 0)
        valid_quote = AssetQuote("PETR4.SA", "Petrobras", 36.5, "BRL", 36.0)
        provider = FallbackDataProvider(
            [StaticProvider(result=invalid_quote), StaticProvider(result=valid_quote)]
        )

        self.assertIs(provider.get_asset_quote("PETR4.SA"), valid_quote)

    def test_raises_error_with_details_when_all_providers_fail(self):
        provider = FallbackDataProvider([StaticProvider(error=ValueError("indisponível"))])

        with self.assertRaisesRegex(ValueError, "indisponível"):
            provider.get_asset_quote("PETR4.SA")


class BrapiProviderTests(unittest.TestCase):
    @patch.dict(os.environ, {"BRAPI_TOKEN": "test-token"})
    @patch("providers.json.load")
    @patch("providers.urlopen")
    def test_maps_quote_and_sends_bearer_token(self, mocked_urlopen, mocked_json_load):
        mocked_urlopen.return_value.__enter__.return_value = Mock()
        mocked_json_load.return_value = {
            "results": [
                {
                    "symbol": "PETR4",
                    "longName": "Petroleo Brasileiro SA",
                    "currency": "BRL",
                    "regularMarketPrice": 36.5,
                    "regularMarketPreviousClose": 36.0,
                    "marketCap": 480000000000,
                }
            ]
        }

        quote = BrapiProvider().get_asset_quote("PETR4.SA")
        request = mocked_urlopen.call_args.args[0]

        self.assertEqual(request.full_url, "https://brapi.dev/api/quote/PETR4")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-token")
        self.assertEqual(quote.current_price, 36.5)
        self.assertEqual(quote.previous_close, 36.0)
        self.assertEqual(quote.source, "Brapi")

    @patch("providers.urlopen", side_effect=HTTPError("https://brapi.dev", 401, "Unauthorized", {}, None))
    def test_explains_unauthorized_token(self, mocked_urlopen):
        with patch.dict(os.environ, {"BRAPI_TOKEN": "test-token"}):
            with self.assertRaisesRegex(ValueError, "Configure BRAPI_TOKEN"):
                BrapiProvider().get_asset_quote("MXRF11.SA")


if __name__ == "__main__":
    unittest.main()