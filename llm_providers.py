from abc import ABC, abstractmethod
import os
import json
from groq import Groq
from dotenv import load_dotenv
from models import AssetQuote, FinancialAnalysis

load_dotenv()

class LLMClient(ABC):
    """Interface para o provedor de Inteligência Artificial."""
    
    @abstractmethod
    def generate_analysis(self, quote: AssetQuote) -> FinancialAnalysis:
        pass

class GroqClient(LLMClient):
    """Implementação usando a API da Groq (gratuita e rápida)."""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
    def generate_analysis(self, quote: AssetQuote) -> FinancialAnalysis:
        prompt = f"""
        Você é um Analista de Sistemas Financeiros sênior. 
        Analise os seguintes dados de mercado e gere um relatório estruturado.
        
        Dados do Ativo:
        - Nome: {quote.name} ({quote.ticker})
        - Preço Atual: {quote.currency} {quote.current_price}
        - Variação Diária: {quote.daily_variation_percent:.2f}%
        - Valor de Mercado: {quote.market_cap}
        - Setor: {quote.sector}
        
        Responda ESTRITAMENTE em formato JSON válido, sem markdown, seguindo esta estrutura:
        {{
            "executive_summary": "...",
            "strengths": ["...", "..."],
            "risks": ["...", "..."],
            "final_verdict": "..."
        }}
        """
        
        response = self.client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {"role": "system", "content": "Você é um analista financeiro que responde apenas em JSON válido."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        json_content = response.choices[0].message.content
        analysis_data = json.loads(json_content)
        
        return FinancialAnalysis(**analysis_data)