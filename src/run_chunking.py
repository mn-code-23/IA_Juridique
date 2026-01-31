from pathlib import Path
from extract_text import extract_text_from_pdf
from chunking import clean_text, split_by_articles
from enricher import enrich_chunk
from vector_store import LegalVectorStore
import logging

logging.getLogger("pdfminer").setLevel(logging.ERROR)

PDF_DIR = Path("../data/pdf")
all_chunks = []

for pdf_file in PDF_DIR.glob("*.pdf"):
    print(f"📄 Traitement : {pdf_file.name}")

    raw_text = extract_text_from_pdf(pdf_file)
    cleaned_text = clean_text(raw_text)
    chunks = split_by_articles(cleaned_text)

    for chunk in chunks:
        chunk["source_pdf"] = pdf_file.name
        chunk = enrich_chunk(chunk)
        all_chunks.append(chunk)

print("\n✅ Enrichissement terminé")
print(f"📦 Total de chunks : {len(all_chunks)}")

# print("\n🧪 Exemple de chunk enrichi :")
# print(all_chunks[0])

# Indexer dans ChromaDB
store = LegalVectorStore()
store.add_chunks(all_chunks)

print("Total chunks dans ChromaDB :", store.count())
print("ChromaDB indexée avec succès")
