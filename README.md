# 🧭 Bússola Capital

**Inteligência para investir.** Um agente de IA que analisa ativos financeiros
(ações, FIIs e criptomoedas) e gera relatórios estruturados com pontos fortes,
riscos e veredito — em uma interface web profissional.

> ⚠️ Projeto educacional. Não é recomendação de investimento.

## 🚀 O que o projeto faz

1. Busca dados reais de mercado via **Yahoo Finance** (`yfinance`), usando a **Brapi** como fallback para ativos da B3
2. Envia os dados a um LLM (**Qwen 3.8 via Groq**) com prompt de analista sênior
3. Valida a resposta da IA contra um contrato **Pydantic** (defesa contra alucinação)
4. Exibe tudo em um dashboard **Streamlit** com métricas, painéis e cards

## 🏗️ Arquitetura

Camadas desacopladas com princípios **SOLID**:

Configure `BRAPI_TOKEN` no ambiente ou em `.streamlit/secrets.toml` para autenticar as consultas à Brapi. Sem token, a API permite apenas os ativos e limites definidos no plano gratuito.
