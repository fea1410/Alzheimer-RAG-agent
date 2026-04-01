from smolagents import TransformersModel, CodeAgent, InferenceClientModel
from retriever import retriever_tool

m1 = 'Qwen/Qwen3-14B'





custom_sys_prompt = '''
When forming your final answer:
1. Extract the 'source' field (PMCID) from every retrieved document
2. Place inline citations [PMCID: PMCxxxxxxx] after EVERY factual claim
3. Never state a drug target without a supporting PMCID — if retriever found nothing relevant, say so explicitly
4. Distinguish between: validated targets, candidate targets, and speculative targets
'''
agent = CodeAgent(
    tools=[retriever_tool],
    model=InferenceClientModel(model_id=m1),
    max_steps=4,
    verbosity_level=2,
    instructions = custom_sys_prompt
)

def rag_agent(query: str):
  return agent.run(query, reset = True)
