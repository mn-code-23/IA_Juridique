# rag_ollama.py
import requests
from vector_store import LegalVectorStore


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # ou "mistral"


SYSTEM_PROMPT = """Tu es une intelligence artificielle juridique spécialisée
exclusivement en droit sénégalais et en droit OHADA.

RÈGLES ABSOLUES :
- Tu réponds UNIQUEMENT à partir des extraits fournis.
- Tu N’INVENTES JAMAIS de loi, d’article ou de jurisprudence.
- Si l’information n’est pas présente dans les sources,
  tu réponds clairement : "Les documents fournis ne permettent pas de répondre."
- Chaque réponse DOIT contenir les références exactes :
  Article + document source.
- Style professionnel, clair, destiné à un avocat.

SOURCES JURIDIQUES :
{context}
"""


class LegalRAG:
    def __init__(self):
        self.store = LegalVectorStore()

    def build_context(self, query, k=5):
        results = self.store.query(query, n_results=k)

        context_blocks = []
        for doc, meta in zip(
            results["documents"][0],
            results["metadatas"][0]
        ):
            block = f"""
Source : {meta.get("source_pdf", "Inconnu")}
Article : {meta.get("article", "Inconnu")}
Texte :
{doc}
"""
            context_blocks.append(block)

        return "\n---\n".join(context_blocks)

    def ask(self, question):
        context = self.build_context(question)

        prompt = SYSTEM_PROMPT.format(context=context) + f"\n\nQUESTION : {question}"

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        return response.json()["response"]
