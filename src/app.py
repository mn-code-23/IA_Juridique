import streamlit as st
from rag_engine import ask_legal_question

st.set_page_config(
    page_title="IA Juridique OHADA",
    layout="wide"
)

# ---------------------------
# SESSION STATE (historique)
# ---------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------
# HEADER
# ---------------------------
st.markdown("""
# IA Juridique – Droit OHADA & Sénégal
**Assistant juridique local et souverain**
""")

st.markdown("---")

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.markdown("## Paramètres")
    st.markdown("• Modèle local Ollama")
    st.markdown("• Données non externalisées")
    st.markdown("---")

    st.markdown("## Historique")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"**{i}.** {item['question'][:60]}...")
    else:
        st.caption("Aucune question posée")

# ---------------------------
# QUESTION
# ---------------------------
st.markdown("## Question juridique")

question = st.text_area(
    label="",
    height=120,
    placeholder="Ex : Quelles sont les conditions de constitution d’une société commerciale selon l’OHADA ?"
)

# ---------------------------
# ACTION
# ---------------------------
if st.button("Analyser juridiquement"):
    if not question.strip():
        st.warning("Veuillez saisir une question juridique.")
    else:
        with st.spinner("Analyse en cours..."):
            response, sources = ask_legal_question(question)

        # Sauvegarde historique
        st.session_state.history.append({
            "question": question,
            "response": response,
            "sources": sources
        })

        st.markdown("---")

        # ---------------------------
        # RÉPONSE
        # ---------------------------
        st.markdown("## Réponse juridique")
        st.write(response)

        # ---------------------------
        # SOURCES
        # ---------------------------
        if sources:
            st.markdown("## Sources juridiques")
            for s in sources:
                st.markdown(
                    f"- **{s['article']}** — *{s['source_pdf']}*"
                )
        else:
            st.caption("Aucune source détectée.")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("Projet IA Juridique – Usage professionnel | 100 % local")
