from sentence_transformers import SentenceTransformer
import chromadb
from config import CHROMA_DIR, COLLECTION_FILES, COLLECTION_FOLDERS, TOP_K_DEFAULT, SNIPPET_BEFORE, SNIPPET_AFTER, MODEL_NAME

# ---------------- INICIALIZAÇÃO ----------------
# Conecta com ChromaDB persistente
client = chromadb.PersistentClient(path=CHROMA_DIR)

# Cria/pega coleções de arquivos e pastas
col_files = client.get_or_create_collection(COLLECTION_FILES)
col_folders = client.get_or_create_collection(COLLECTION_FOLDERS)

# Carrega modelo de embeddings
sbert = SentenceTransformer(MODEL_NAME)

# ---------------- FUNÇÕES ----------------
def embed_query(texto: str):
    """
    Recebe uma string e retorna o embedding vetorial correspondente.
    """
    emb = sbert.encode([texto], show_progress_bar=False, convert_to_tensor=False)[0]
    # Garante que o embedding seja uma lista de floats
    return emb.tolist() if hasattr(emb, "tolist") else list(map(float, emb))

def extract_snippet(texto: str, consulta: str, before=SNIPPET_BEFORE, after=SNIPPET_AFTER):
    """
    Retorna um trecho do texto com o termo da consulta destacado (**term**),
    com 'before' caracteres antes e 'after' depois do termo.
    """
    if not texto:
        return None
    texto_str = str(texto)
    idx = texto_str.lower().find(consulta.lower())  # busca case-insensitive
    if idx == -1:
        # se termo não encontrado, retorna início do texto
        snippet = texto_str[:after].replace("\n", " ")
        return snippet + ("..." if len(texto_str) > after else "")
    start = max(idx - before, 0)
    end = min(idx + len(consulta) + after, len(texto_str))
    raw = texto_str[start:end].replace("\n", " ")
    highlight_start = idx - start
    highlight_end = highlight_start + len(consulta)
    # adiciona ** para destacar o termo
    return raw[:highlight_start] + "**" + raw[highlight_start:highlight_end] + "**" + raw[highlight_end:]

def pesquisar_chroma(consulta, top_k=TOP_K_DEFAULT, tipo="both"):
    """
    Pesquisa no ChromaDB os documentos e pastas mais similares à consulta.
    Retorna um dicionário com resultados:
    {
        "Arquivos": [{"path": ..., "snippet": ..., "score": ...}, ...],
        "Pastas": [{"path": ..., "snippet": ..., "score": ...}, ...]
    }
    """
    query_emb = embed_query(consulta)
    resultados = {}
    if tipo in ["arquivo", "both"]:
        r_files = col_files.query(query_embeddings=[query_emb], n_results=top_k,
                                  include=["documents","metadatas","distances"])
        resultados["Arquivos"] = [{"path": m.get("path") or m.get("nome","sem caminho"),
                                    "snippet": extract_snippet(d, consulta),
                                    "score": s}
                                   for d,m,s in zip(r_files["documents"][0],
                                                    r_files["metadatas"][0],
                                                    r_files["distances"][0])]
    if tipo in ["pasta", "both"]:
        r_folders = col_folders.query(query_embeddings=[query_emb], n_results=top_k,
                                      include=["documents","metadatas","distances"])
        resultados["Pastas"] = [{"path": m.get("path") or m.get("nome","sem caminho"),
                                 "snippet": extract_snippet(d, consulta),
                                 "score": s}
                                for d,m,s in zip(r_folders["documents"][0],
                                                 r_folders["metadatas"][0],
                                                 r_folders["distances"][0])]
    return resultados
