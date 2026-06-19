from services.retrieval_service import RetrievalService
from services.llm_service import LLMService
from services.memory_service import MemoryService

retrieval_service = RetrievalService()
llm_service = LLMService()
memory_service = MemoryService()


def generate_answer(
    message: str,
    session_id: str
):

    # Load previous conversation
    history_text = memory_service.get_history_text(
        session_id,
        limit=4
    )

    # Retrieve relevant document chunks
    context = retrieval_service.build_context(
        message
    )

    print("DEBUG CONTEXT LENGTH:", len(context))
    print("DEBUG HISTORY:", history_text[:300])
    print("=" * 50)
    print("HISTORY LENGTH:", len(history_text))
    print("CONTEXT LENGTH:", len(context))
    print("=" * 50)

    if not context:
        answer = "No relevant context found in documents."

        memory_service.save_message(
            session_id,
            "user",
            message
        )

        memory_service.save_message(
            session_id,
            "assistant",
            answer
        )

        return answer

    # Safety limit
    if len(context) > 800:
        context = context[:800]

    prompt = f"""
You are a helpful assistant.

Use the conversation history and document context to answer.

If the answer is not found in the document context, say you don't know.

Conversation History:
{history_text}

Document Context:
{context}

Question:
{message}

Answer:
"""

    answer = llm_service.generate(prompt)

    # Save user message
    memory_service.save_message(
        session_id,
        "user",
        message
    )

    # Save assistant response
    memory_service.save_message(
        session_id,
        "assistant",
        answer
    )

    return answer