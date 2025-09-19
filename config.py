# ---------------- CONFIGURAÇÕES GLOBAIS ----------------
# Pasta onde o ChromaDB vai ser salvo / lido
CHROMA_DIR = "./chroma_db"

# Nomes das coleções no ChromaDB
COLLECTION_FILES = "files_name"   # coleção de arquivos
COLLECTION_FOLDERS = "folders"    # coleção de pastas

# Parâmetros de pesquisa
TOP_K_DEFAULT = 3       # quantidade padrão de resultados retornados
SNIPPET_BEFORE = 30     # número de caracteres antes do termo encontrado
SNIPPET_AFTER = 200     # número de caracteres depois do termo encontrado

# Modelo para embeddings
MODEL_NAME = "all-MiniLM-L6-v2"   # modelo SentenceTransformer
