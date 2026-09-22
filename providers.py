from abc import ABC, abstractmethod
import yfinance as yf
from models import AssetQuote

class DataProvider(ABC):
    """Interface abstrata para provedores de dados financeiros."""
    
    @abstractmethod
    def get_asset_quote(self, ticker: str) -> AssetQuote:
        pass

class YahooFinanceProvider(DataProvider):
    """Implementação concreta usando a biblioteca yfinance."""
    
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
                sector=info.get("sector")
            )
        except Exception as e:
            raise ValueError(f"Erro ao buscar dados para o ticker {ticker}: {e}")