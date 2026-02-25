from vector_store import LegalVectorStore
import subprocess
import textwrap

# -----------------------------
# PARAMÈTRES CRITIQUES
# -----------------------------
K = 5
MAX_CONTEXT_CHARS = 2500
MAX_RESPONSE_TOKENS = 256
MODEL = "llama3"  # ou "qwen2.5:3b"


# -----------------------------
# QUESTION TEST
# -----------------------------
# question = (
#     "Quelles sont les règles applicables à la vente commerciale "
#     "dans le droit OHADA ?"
# )

question = ("Quelles sont les conditions de constitution d’une société commerciale selon l’OHADA ?")

# -----------------------------
# CHARGEMENT CHROMADB
# -----------------------------
print("Chargement de ChromaDB...")
vectorstore = LegalVectorStore()

results = vectorstore.query(question, n_results=K)

# -----------------------------
# CONSTRUCTION DU CONTEXTE
# -----------------------------
context = ""
for doc_text in results["documents"][0]:
    if len(context) + len(doc_text) > MAX_CONTEXT_CHARS:
        break
    context += doc_text.strip() + "\n\n"

print("===== CONTEXTE ENVOYÉ AU LLM =====")
print(context[:2000])
print("=================================")

# -----------------------------
# PROMPT JURIDIQUE MINIMAL
# -----------------------------
prompt = f"""
Tu es un assistant juridique expert en droit OHADA.

Ta réponse doit être fondée UNIQUEMENT sur les extraits fournis.
Tu dois citer les articles lorsqu'ils apparaissent.

Si et seulement si l'information est absente du contexte,
réponds exactement :
"Information non trouvée dans les documents."

CONTEXTE JURIDIQUE :
{context}

QUESTION :
{question}

RÉPONSE JURIDIQUE :
"""


prompt = textwrap.dedent(prompt).strip()

# -----------------------------
# APPEL OLLAMA (SÉCURISÉ)
# -----------------------------
print("Interrogation du modèle...")

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
    stdout, stderr = process.communicate(prompt, timeout=180)
except subprocess.TimeoutExpired:
    process.kill()
    raise RuntimeError("Timeout Ollama — génération trop lente")

print("\nRÉPONSE DU MODÈLE :\n")
print(stdout.strip())
