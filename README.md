# Agente Inteligente com LangChain e Ollama (Llama 3) 🤖

Este projeto é um agente inteligente construído com Python e LangChain, capaz de decidir autonomamente quando usar seu conhecimento geral ou acionar uma ferramenta de calculadora exata.

## 🛠️ Tecnologias Utilizadas
* **Python 3.12**
* **LangChain** (Framework de orquestração)
* **Ollama** (Rodando o modelo **Llama 3** 100% localmente)
* **Numexpr** (Motor matemático para a ferramenta de calculadora)

## 🧠 Como Funciona (Ciclo ReAct)
O agente utiliza o framework de raciocínio ReAct (Reasoning and Acting). Ao receber um comando em texto:
1. **Conhecimentos Gerais:** Se a pergunta for sobre história, programação ou atualidades, o modelo responde usando sua própria base de dados.
2. **Matemática:** Se identificar uma operação matemática, ele aciona a `Calculadora` personalizada, executa a equação de forma imune a alucinações e formula a resposta final.

## 🚀 Como Executar Localmente
1. Instale o [Ollama](https://ollama.com/) e baixe o modelo Llama 3 (`ollama run llama3`).
2. Clone este repositório.
3. Crie um ambiente virtual: `python -m venv venv`
4. Ative o ambiente e instale as dependências: `pip install -r requirements.txt`
5. Execute o agente: `python main.py`