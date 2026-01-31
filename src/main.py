from extract_text import extract_text_from_pdf
from chunking import clean_text, split_by_articles

pdf_path = "../data/pdf/Acte-uniforme-relatif-droit-societes-commerciales-gie-auscgie-jo-fevrier-2014.pdf"

raw_text = extract_text_from_pdf(pdf_path)
cleaned_text = clean_text(raw_text)
chunks = split_by_articles(cleaned_text)

print(f"Nombre de chunks : {len(chunks)}")
print(chunks[0])
