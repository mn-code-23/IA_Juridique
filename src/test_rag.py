from rag_ollama import LegalRAG

rag = LegalRAG()

question = "Quelles sont les conditions de constitution d’une société commerciale selon l’OHADA ?"

answer = rag.ask(question)

print("\n🔎 QUESTION :")
print(question)

print("\n⚖️ RÉPONSE JURIDIQUE :")
print(answer)
