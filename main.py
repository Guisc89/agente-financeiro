from providers import YahooFinanceProvider
from llm_providers import GroqClient
from agent_core import FinancialAgent

if __name__ == "__main__":
    # 1. Instanciamos as dependências concretas
    data_provider = YahooFinanceProvider()
    llm_client = GroqClient() # Usando a Groq agora!
    
    # 2. Injetamos tudo no nosso Agente
    agent = FinancialAgent(data_provider=data_provider, llm_client=llm_client)
    
    # 3. Escolha o ativo para testar (Lembre-se: ações do Brasil levam .SA)
    ticker_alvo = "MXRF11.SA" 
    
    try:
        # Executa a mágica
        resultado = agent.run_analysis(ticker_alvo)
        
        # 4. Exibe o relatório formatado
        print("\n" + "="*50)
        print(f"📊 RELATÓRIO FINANCEIRO: {ticker_alvo}")
        print("="*50)
        print(f"📝 Resumo Executivo: {resultado.executive_summary}")
        
        print(f"\n✅ Pontos Fortes:")
        for point in resultado.strengths:
            print(f"   - {point}")
            
        print(f"\n⚠️ Riscos e Alertas:")
        for risk in resultado.risks:
            print(f"   - {risk}")
            
        print(f"\n🎯 Veredito Final: {resultado.final_verdict}")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Ocorreu um erro na análise: {e}")