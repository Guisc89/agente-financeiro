# 🧭 Bússola Capital

**Inteligência para investir.** Um agente de IA que analisa ativos financeiros
(ações, FIIs e criptomoedas) e gera relatórios estruturados com pontos fortes,
riscos e veredito — em uma interface web profissional.

> ⚠️ Projeto educacional. Não é recomendação de investimento.

## 🚀 O que o projeto faz

1. Busca dados reais de mercado via **Yahoo Finance** (`yfinance`), usando a **Brapi** como fallback para ativos da B3
2. Envia os dados a um LLM (**Qwen 3.8 via Groq**) com prompt de analista sênior
3. Valida a resposta da IA contra um contrato **Pydantic** (defesa contra alucinação)
4. Permite selecionar ações e FIIs da B3 em uma lista pesquisável na lateral
5. Exibe os dados em um dashboard **Streamlit** com conteúdo educativo sobre ações, FIIs, ETFs, BDRs e riscos

## 🏗️ Arquitetura

Camadas desacopladas com princípios **SOLID**:

Configure `BRAPI_TOKEN` no ambiente ou em `.streamlit/secrets.toml` para autenticar as consultas à Brapi. No Streamlit Community Cloud, adicione `BRAPI_TOKEN = "seu_token"` em **App settings → Secrets**. Sem token, a API permite apenas os ativos e limites definidos no plano gratuito.

No Streamlit Community Cloud, apps sem tráfego por 12 horas hibernam e acordam quando alguém os visita. Esse comportamento da hospedagem não é desativado por uma configuração no app; para disponibilidade contínua, use uma hospedagem sempre ativa.
