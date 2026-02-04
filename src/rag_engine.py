from vector_store import LegalVectorStore
import subprocess
import textwrap

MODEL = "qwen2.5:3b"
K = 5
MAX_CONTEXT_CHARS = 2500
TIMEOUT = 180

vectorstore = LegalVectorStore()

def ask_legal_question(question: str):
    results = vectorstore.query(question, n_results=K)

    context = ""
    sources = []

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        if len(context) + len(doc) > MAX_CONTEXT_CHARS:
            break

        context += doc.strip() + "\n\n"

        sources.append({
            "article": meta.get("article", "Article ?"),
            "source_pdf": meta.get("source_pdf", "Document inconnu")
        })

    prompt = f"""
Tu es un assistant juridique spécialisé en droit OHADA et sénégalais.

Réponds exclusivement à partir des documents fournis.
Cite les articles lorsqu'ils sont mentionnés.

CONTEXTE :
{context}

QUESTION :
{question}

RÉPONSE :
"""
    prompt = textwrap.dedent(prompt).strip()

    process = subprocess.Popen(
        ["ollama", "run", MODEL],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    try:
        stdout, _ = process.communicate(prompt, timeout=TIMEOUT)
        return stdout.strip(), sources
    except Exception:
        process.kill()
        return "Erreur lors de la génération.", sources
