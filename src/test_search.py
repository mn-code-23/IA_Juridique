from vector_store import LegalVectorStore

store = LegalVectorStore()
print("Chunks :", store.count())

res = store.query(
    "conditions de constitution d'une société commerciale",
    n_results=3
)

for i, doc in enumerate(res["documents"][0]):
    print("\nRésultat", i+1)
    print(res["metadatas"][0][i]["article"])
    print(doc[:300], "...")
