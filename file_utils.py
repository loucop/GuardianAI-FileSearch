import os
import subprocess

# ---------------- FUNÇÕES DE ARQUIVO / PASTA ----------------

def abrir_arquivo(caminho):
    """
    Abre um arquivo no Windows Explorer usando o caminho completo.
    """
    if os.path.exists(caminho):
        os.startfile(caminho)  # equivalente a dar duplo clique no arquivo

def abrir_pasta(caminho):
    """
    Abre a pasta que contém o arquivo e seleciona o arquivo no Explorer.
    """
    if os.path.exists(caminho):
        subprocess.run(f'explorer /select,"{caminho}"')
