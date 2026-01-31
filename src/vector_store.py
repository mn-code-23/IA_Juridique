# vector_store.py
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer


class LegalVectorStore:
    def __init__(self, persist_directory="../chroma_db", collection_name="ia_juridique"):
        """
        Initialise ChromaDB avec persistance automatique (Chroma v0.5+)
        """
        self.client = PersistentClient(path=persist_directory)

        existing = [c.name for c in self.client.list_collections()]
        if collection_name in existing:
            self.collection = self.client.get_collection(collection_name)
        else:
            self.collection = self.client.create_collection(name=collection_name)

        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

    def add_chunks(self, chunks):
        texts = []
        metadatas = []

        for c in chunks:
            texts.append(c.get("text", ""))

            md = {}
            for k, v in c.items():
                if k != "text":
                    md[k] = "" if v is None else str(v)
            metadatas.append(md)

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        ids = [f"chunk_{i}" for i in range(len(chunks))]

        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings
        )

        print(f"{len(chunks)} chunks indexés et persistés dans ChromaDB")

    def query(self, query_text, n_results=5):
        query_embedding = self.model.encode(
            [query_text], convert_to_numpy=True
        )

        return self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )

    def count(self):
        return self.collection.count()
