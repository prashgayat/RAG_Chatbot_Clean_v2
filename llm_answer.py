import os
from dotenv import load_dotenv
import openai
from retriever_utils import hybrid_retriever

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Build the full prompt
def build_prompt(context_chunks, question):
    context_text = "\n\n---\n\n".join([doc.page_content for doc in context_chunks])
    prompt = f"""
You are a helpful assistant answering questions strictly based on the provided context.

Context:
{context_text}

Question:
{question}

If the answer cannot be found in the context, reply with:
"I'm sorry, I couldn't find the answer in the provided documents."
"""
    return prompt.strip()

# Main LLM call logic
def llm_answer(query, session_id=None):
    try:
        # Step 1: Retrieve context
        relevant_docs = hybrid_retriever(query, k=5, rerank=True)

        if not relevant_docs:
            return "I'm sorry, I couldn't find anything relevant in the documents."

        # Step 2: Build prompt with selected chunks
        prompt = build_prompt(relevant_docs, query)

        # Step 3: Query OpenAI LLM
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers based only on provided document context."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Error during answer generation: {str(e)}"
