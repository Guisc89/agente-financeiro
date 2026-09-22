from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field

@dataclass
class AssetQuote:
    """DTO para representar a cotação atual de um ativo."""
    ticker: str
    name: str
    current_price: float
    currency: str
    previous_close: float
    market_cap: Optional[float] = None
    sector: Optional[str] = None
    
    @property
    def daily_variation_percent(self) -> float:
        """Calcula a variação diária em porcentagem (Encapsulamento de lógica)."""
        if self.previous_close == 0:
            return 0.0
        return ((self.current_price - self.previous_close) / self.previous_close) * 100
    
class FinancialAnalysis(BaseModel):
    """Estrutura obrigatória para a resposta do Analista de IA."""
    executive_summary: str = Field(description="Resumo curto e objetivo da situação do ativo")
    strengths: List[str] = Field(description="Lista de pontos fortes ou indicadores positivos")
    risks: List[str] = Field(description="Lista de riscos, alertas ou pontos de atenção")
    final_verdict: str = Field(description="Conclusão final do analista (ex: 'Manter', 'Comprar', 'Vender')")