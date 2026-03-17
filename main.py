from langchain_ollama import OllamaLLM
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
import numexpr as ne

# 1. LLM com as travas de parada
llm = OllamaLLM(model="llama3", temperature=0).bind(
    stop=["\nObservation:", "Observation:"]
)

# 2. Ferramenta de Calculadora Segura
def calcular_matematica(expressao: str) -> str:
    try:
        expressao_limpa = expressao.replace('`', '').strip()
        return str(ne.evaluate(expressao_limpa))
    except Exception as e:
        return "Erro na equação."

ferramenta_calculadora = Tool(
    name="Calculadora",
    func=calcular_matematica,
    description="Calculadora matemática. Aceita APENAS equações exatas (ex: 850 * 0.15)."
)

ferramentas = [ferramenta_calculadora]

# 3. Prompt ReAct "Few-Shot" CORRIGIDO
template = '''Você é um assistente super inteligente. Responda em português.
Você tem acesso às seguintes ferramentas: {tools}
O nome da ferramenta a ser usada deve ser exatamente um destes: {tool_names}

REGRAS DE OURO:
1. Se a pergunta for de MATEMÁTICA, você DEVE usar a ferramenta Calculadora.
2. Se a pergunta for sobre QUALQUER OUTRA COISA (história, pessoas, textos), NÃO USE A FERRAMENTA. Use seu conhecimento e vá direto para a resposta final.

== EXEMPLO DE COMO AGIR COM MATEMÁTICA ==
Question: Quanto é 25 * 4?
Thought: É uma conta matemática, vou usar a ferramenta.
Action: Calculadora
Action Input: 25 * 4
Observation: 100
Thought: Agora sei a resposta.
Final Answer: O resultado é 100.

== EXEMPLO DE COMO AGIR COM ASSUNTOS GERAIS ==
Question: Quem descobriu o Brasil?
Thought: Isso é história, não preciso de calculadora.
Final Answer: Pedro Álvares Cabral descobriu o Brasil em 1500.

Comece! Siga estritamente o formato dos exemplos acima.

Question: {input}
Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)

# 4. Inicializa o Agente Inteligente
agente_react = create_react_agent(llm, ferramentas, prompt)
agente_executor = AgentExecutor(
    agent=agente_react, 
    tools=ferramentas, 
    verbose=True, 
    handle_parsing_errors=True,
    max_iterations=5
)

# 5. Loop de interação
print("\n🤖 Agente Inteligente Iniciado! (Digite 'sair' para encerrar)")
print("-" * 50)

while True:
    pergunta = input("\nFaça uma pergunta: ")
    
    if pergunta.lower() in ['sair', 'exit', 'quit']:
        print("Encerrando o agente...")
        break
        
    try:
        resposta = agente_executor.invoke({"input": pergunta})
        print("\n=== RESPOSTA FINAL ===")
        print(resposta["output"])
    except Exception as e:
        print(f"\n[Erro na execução]: {e}")