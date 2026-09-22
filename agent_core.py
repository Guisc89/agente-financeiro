from typing import Optional

from providers import DataProvider
from llm_providers import LLMClient
from models import AssetQuote, FinancialAnalysis


class FinancialAgent:
    """O Agente principal. Orquestra dados e IA."""

    def __init__(self, data_provider: DataProvider, llm_client: LLMClient):
        self.data_provider = data_provider
        self.llm_client = llm_client

    def get_quote(self, ticker: str) -> AssetQuote:
        """Expõe a busca de cotação para uso externo (ex.: interface)."""
        return self.data_provider.get_asset_quote(ticker)

    def run_analysis(self, ticker: str, quote: Optional[AssetQuote] = None) -> FinancialAnalysis:
        if quote is None:
            quote = self.get_quote(ticker)

        print("🧠 Processando análise com IA...")
        return self.llm_client.generate_analysis(quote)