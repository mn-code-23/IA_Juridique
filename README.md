# 🏛️ IA Juridique - RAG LegalTech

Système d'IA juridique spécialisé en **droit sénégalais** et **droit OHADA**, basé sur Retrieval-Augmented Generation (RAG) avec Ollama et ChromaDB.

## 📋 Vue d'ensemble

Ce projet implémente une solution RAG pour :
- 📄 Extraire et indexer des documents juridiques (PDF)
- 🔍 Rechercher des informations pertinentes par similarité sémantique
- 🧠 Générer des réponses précises avec le modèle LLaMA 3 (Ollama)
- ⚖️ Garantir des réponses basées exclusivement sur les sources fournies

## 🚀 Prérequis

- **Python 3.10+**
- **Ollama** installé ([télécharger](https://ollama.ai))
- **LLaMA 3** téléchargé : `ollama pull llama3`

## 📦 Installation

### 1. Cloner ou créer l'environnement virtuel

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Vérifier Ollama

```bash
ollama serve  # Démarrer le serveur (port 11434)
```

## 📁 Structure du projet

```
IA_LegalTech/
├── src/
│   ├── main.py                 # Workflow principal
│   ├── extract_text.py         # Extraction de texte PDF
│   ├── chunking.py             # Segmentation par articles
│   ├── metadata.py             # Métadonnées des documents
│   ├── vector_store.py         # Gestion ChromaDB + embeddings
│   ├── rag_ollama.py           # Pipeline RAG avec Ollama
│   ├── enricher.py             # Enrichissement du contexte
│   ├── run_chunking.py         # Script de chunking
│   ├── index_chunks.py         # Indexation des chunks
│   ├── test_rag.py             # Tests du RAG
│   ├── test_rag_anti-crash.py  # Tests robustes avec timeout
│   └── test_search.py          # Tests de recherche vectorielle
├── data/
│   └── pdf/                    # Documents juridiques (PDF)
├── chroma_db/                  # Base de données vectorielle persistante
├── requirements.txt            # Dépendances Python
└── README.md                   # Ce fichier
```

## 🔄 Workflow

### 1. **Extraction, chunking et Indexation** (run_chunking.py)

```bash
python src/run_chunking.py
```

- Extrait le texte des fichiers PDF
- Nettoie et formate le texte
- Segmente par articles juridiques
- Crée les embeddings avec `sentence-transformers`
- Stocke les chunks dans ChromaDB
- Indexe les documents pour la recherche
- Génère des métadonnées


### 2. **Interrogation du RAG** (test_rag_anti-crash.py)

```bash
python src/test_rag_anti-crash.py
```

- Pose une question juridique
- Récupère les chunks pertinents via recherche vectorielle
- Génère une réponse précise avec qwen2.5:3b
- Inclut un timeout de 60s pour éviter les blocages

- Sa marche sans probleme executer de fichier alors

```bash
python src/test_rag.py
```

## 🛠️ Fichiers clés

### `vector_store.py`
Gestion de la base de données vectorielle :
- ChromaDB pour la persistance
- Embeddings multilingues (paraphrase-multilingual-MiniLM-L12-v2)
- Recherche par similarité sémantique

```python
from vector_store import LegalVectorStore
vectorstore = LegalVectorStore()
results = vectorstore.query("Question juridique", n_results=2)
```

### `rag_ollama.py`
Pipeline RAG complet :
- Récupération du contexte depuis ChromaDB
- Construction du prompt avec contraintes absolues
- Appel à Ollama avec gestion d'erreurs
- Extraction des références juridiques

### `extract_text.py`
Extraction de texte PDF :
- Support des documents multilingues
- Nettoyage automatique
- Extraction de métadonnées

### `chunking.py`
Segmentation intelligente :
- Division par articles (structure juridique)
- Préservation du contexte
- Métadonnées par chunk

## ⚙️ Configuration

### Paramètres du RAG (test_rag_anti-crash.py)

```python
K = 5                          # Nombre de chunks récupérés
MAX_CONTEXT_CHARS = 2500        # Limite de contexte
MAX_RESPONSE_TOKENS = 256      # Réponses courtes
MODEL = "qwen2.5:3b"               # Modèle LLM
TIMEOUT = 180                   # Timeout en secondes
```

### Paramètres du RAG (test_rag.py)

```python
MODEL = "llama3"               # Modèle LLM
```

### Paramètres ChromaDB

```python
persist_directory = "../chroma_db"  # Dossier de persistance
collection_name = "ia_juridique"    # Nom de la collection
```

## 🧪 Tests

### Test RAG robuste
```bash
python src/test_rag_anti-crash.py
```
Inclut gestion du timeout et des erreurs.

### Test de recherche vectorielle
```bash
python src/test_search.py
```
Valide les embeddings et la recherche.

### Test RAG standard
```bash
python src/test_rag.py
```

## 🌐 Interface Streamlit

### Installation de Streamlit

Streamlit est déjà inclus dans `requirements.txt`. Si vous ne l'avez pas installé :

```bash
pip install streamlit
```

### Lancement de l'interface

Avec l'environnement virtuel activé :

```bash
streamlit run src/app.py
```

Ou si vous êtes dans le répertoire `src/` :

```bash
streamlit run app.py
```

### Accès à l'interface

Une fois lancée, l'interface Streamlit est accessible à l'adresse :

```
http://localhost:8501
```

### Fonctionnalités de l'interface

L'application `app.py` offre une interface web pour :
- 💬 Poser des questions juridiques en français
- 📚 Consulter les documents indexés
- 🔍 Visualiser les chunks pertinents retrouvés
- ⚖️ Recevoir des réponses basées sur le droit sénégalais et OHADA
- 📄 Voir les sources et références des réponses

### Configuration du port

Si le port 8501 est occupé, vous pouvez spécifier un autre port :

```bash
streamlit run src/app.py --server.port 8502
```

### Arrêt de l'application

Pour arrêter le serveur Streamlit, appuyez sur `Ctrl+C` dans le terminal.

## 📊 Améliorations et optimisations

✅ **Paramétrisation rapide** : K=1, tokens réduits, timeouts courts  
✅ **Gestion robuste** : Try-catch, timeouts Ollama, cleanup des processus  
✅ **Multilingue** : Embeddings français + anglais  
✅ **Persistance** : ChromaDB sauvegarde automatiquement  

## 🚨 Dépannage

### Timeout Ollama
```
subprocess.TimeoutExpired: Command 'ollama run llama3' timed out after 60 seconds
```
**Solution** : Réduire `MAX_CONTEXT_CHARS` ou `MAX_RESPONSE_TOKENS`

### ChromaDB introuvable
```
FileNotFoundError: chroma_db not found
```
**Solution** : Lancer d'abord `python src/run_chunking.py` pour créer la base

### Ollama non disponible
```
ConnectionRefusedError: [Errno 10061] No connection could be made
```
**Solution** : Démarrer Ollama : `ollama serve`

## 📚 Dépendances principales

- **chromadb** : Base de données vectorielle
- **sentence-transformers** : Embeddings multilingues
- **ollama** : Interface LLM locale
- **pypdf** : Extraction PDF
- **pydantic** : Validation de données

## 📝 Conventions

- 🔎 **Recherche** : K=1-2 chunks max (performance)
- 📏 **Contexte** : Max 800-1500 caractères
- ⏱️ **Timeout** : 60-180 secondes selon le contexte
- 📌 **Métadonnées** : Source + article obligatoires

## 🔐 Sécurité et conformité

✅ **Pas d'hallucinations** : Réponses basées uniquement sur les sources  
✅ **Références juridiques** : Articles + documents toujours cités  
✅ **Local & Privé** : Aucune donnée envoyée à l'externe  
✅ **Sénégalais/OHADA** : Modèle spécialisé en droit régional  

## 📞 Support

Pour toute issue ou amélioration, consultez la structure du code et les logs détaillés dans les fichiers de test.

---

**Dernière mise à jour** : Janvier 2026  
**Status** : Production-ready avec gestion d'erreurs robuste ✅


# Si vous etes trop parresseur pour lire tout le fichier (mdr) voici un resume pour les commandes a faire 

# 1. Telecharger et Intaller Ollama dans votre PC 

### Installer git et python(3.13.7 ou +3.10) sur votre machine si ce n'est pas encore fait 

# 2. Installer ces 2 modeles suivantes dans votre CMD
--> ollama pull llama3 (modele principal mais un peu lourd)
--> ollama pull qwen2.5:3b (modele secondaire plus leger pour tester notre IA)

# 1. Créer son propre environnement
python -m venv venv

# 2. L'activer
source venv/bin/activate  # Sur Mac/Linux
.\venv\Scripts\activate   # Sur Windows

# 3. Cloner le depot git
git clone https://github.com/mn-code-23/IA_Juridique

# 4. Installer TOUT ton projet d'un coup
pip install -r requirements.txt

# 5. Lancer le fichier test_rag.py
python test_rag.py
- Si ca fait planter votre machine (mdr) arreter l'execution et lancer de fichier
python test_rag_anti-crash.py
