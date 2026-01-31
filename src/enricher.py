from metadata import PDF_METADATA

def enrich_chunk(chunk: dict) -> dict:
    pdf_name = chunk["source_pdf"]

    for key, meta in PDF_METADATA.items():
        if key.lower() in pdf_name.lower():
            chunk.update(meta)
            return chunk

    # fallback si inconnu
    chunk.update({
        "juridiction": "INCONNU",
        "texte": pdf_name,
        "annee": None,
        "type_texte": "INCONNU"
    })
    return chunk
