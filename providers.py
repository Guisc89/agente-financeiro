from abc import ABC, abstractmethod
import json
import os
from typing import List, Optional
from urllib.parse import quote
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import yfinance as yf
from models import AssetQuote

class DataProvider(ABC):
    """Interface abstrata para provedores de dados financeiros."""
    
    @abstractmethod
    def get_asset_quote(self, ticker: str) -> AssetQuote:
        pass

class YahooFinanceProvider(DataProvider):
    """Implementação concreta usando a biblioteca yfinance."""

    source_name = "Yahoo Finance"
    
    def get_asset_quote(self, ticker: str) -> AssetQuote:
        try:
            # Busca o ticker no Yahoo Finance
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Mapeia os dados brutos para o nosso DTO (Data Transfer Object)
            return AssetQuote(
                ticker=ticker.upper(),
                name=info.get("longName", ticker),
                current_price=info.get("regularMarketPrice", 0.0),
                currency=info.get("currency", "BRL"),
                previous_close=info.get("regularMarketPreviousClose", 0.0),
                market_cap=info.get("marketCap"),
                sector=info.get("sector"),
                source=self.source_name,
            )
        except Exception as e:
            raise ValueError(f"Erro ao buscar dados para o ticker {ticker}: {e}")


class BrapiProvider(DataProvider):
    """Implementação usando a API de cotações da Brapi para ativos da B3."""

    source_name = "Brapi"

    def get_asset_quote(self, ticker: str) -> AssetQuote:
        brapi_ticker = ticker.upper().removesuffix(".SA")
        url = f"https://brapi.dev/api/quote/{quote(brapi_ticker, safe='')}"
        headers = {"Accept": "application/json"}
        token = os.getenv("BRAPI_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            request = Request(url, headers=headers)
            with urlopen(request, timeout=10) as response:
                payload = json.load(response)

            results = payload.get("results", [])
            if not results:
                detail = payload.get("message") or payload.get("error") or "ticker não encontrado"
                raise ValueError(detail)

            info = results[0]
            price = info.get("regularMarketPrice")
            if price is None or float(price) <= 0:
                raise ValueError("a resposta não contém um preço válido")

            market_cap = info.get("marketCap")
            return AssetQuote(
                ticker=ticker.upper(),
                name=info.get("longName") or info.get("shortName") or brapi_ticker,
                current_price=float(price),
                currency=info.get("currency") or "BRL",
                previous_close=float(info.get("regularMarketPreviousClose") or 0.0),
                market_cap=float(market_cap) if market_cap is not None else None,
                sector=info.get("sector"),
                source=self.source_name,
            )
        except HTTPError as e:
            if e.code == 401:
                detail = (
                    "HTTP 401: token ausente ou inválido. Configure BRAPI_TOKEN "
                    "nas Secrets do Streamlit Cloud ou no ambiente local."
                )
                raise ValueError(
                    f"Erro ao buscar dados na Brapi para o ticker {ticker}: {detail}"
                ) from e
            raise ValueError(f"Erro ao buscar dados na Brapi para o ticker {ticker}: {e}") from e
        except Exception as e:
            raise ValueError(f"Erro ao buscar dados na Brapi para o ticker {ticker}: {e}") from e


class FallbackDataProvider(DataProvider):
    """Tenta provedores em ordem e retorna a primeira cotação utilizável."""

    def __init__(self, providers: Optional[List[DataProvider]] = None):
        self.providers = providers if providers is not None else [
            YahooFinanceProvider(),
            BrapiProvider(),
        ]

    def get_asset_quote(self, ticker: str) -> AssetQuote:
        errors = []
        for provider in self.providers:
            try:
                quote = provider.get_asset_quote(ticker)
                if quote.current_price <= 0:
                    raise ValueError("o provedor retornou um preço inválido")
                return quote
            except Exception as e:
                source = getattr(provider, "source_name", provider.__class__.__name__)
                errors.append(f"{source}: {e}")

        details = " | ".join(errors) or "nenhum provedor configurado"
        raise ValueError(f"Não foi possível buscar dados para o ticker {ticker}. {details}")