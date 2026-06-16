from services.retrieval_service import RetrievalService
from services.llm_service import LLMService  # example abstraction

retrieval_service = RetrievalService()
llm_service = LLMService()

def generate_answer(message: str):

    context = retrieval_service.build_context(message)

    # 🔥 safety guard
    if len(context) > 1500:
        context = context[:1500]

    prompt = f"""
You are a helpful assistant.

Use ONLY the context below. If answer is not in context, say you don't know.

Context:
{context}

Question:
{message}

Answer:
"""

    return llm_service.generate(prompt)