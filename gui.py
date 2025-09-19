import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial
from ai_utils import pesquisar_chroma
from file_utils import abrir_arquivo, abrir_pasta

class FileSearchApp:
    """
    Classe principal da GUI do Guardian AI FileSearch.
    Contém toda a interface Tkinter e lógica de exibição de resultados.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Guardian AI FileSearch 1.0")
        self.root.geometry("900x600")
        self.root.iconbitmap("icone.ico")  # ícone da janela
        self.root.configure(bg="#f0f4f8")

        # ---------------- FRAME SUPERIOR ----------------
        top_frame = tk.Frame(root, bg="#f0f4f8", pady=5)
        top_frame.pack(fill="x")

        # Campo de pesquisa
        tk.Label(top_frame, text="Pesquisar:", bg="#f0f4f8").pack(side="left", padx=(10,5))
        self.query_entry = tk.Entry(top_frame, width=40)
        self.query_entry.pack(side="left", padx=(0,10))

        # Campo Top N
        tk.Label(top_frame, text="Top N:", bg="#f0f4f8").pack(side="left")
        self.top_var = tk.IntVar(value=3)
        ttk.Combobox(top_frame, textvariable=self.top_var, values=[1,2,3,4,5], width=3).pack(side="left", padx=(0,10))

        # Campo Tipo (Arquivo / Pasta / Ambos)
        tk.Label(top_frame, text="Tipo:", bg="#f0f4f8").pack(side="left")
        self.type_var = tk.StringVar(value="Ambos")
        ttk.Combobox(top_frame, textvariable=self.type_var, values=["Arquivo","Pasta","Ambos"], width=6).pack(side="left", padx=(0,10))

        # Botões de ação
        tk.Button(top_frame, text="Pesquisar", command=self.run_search, bg="#3b82f6", fg="white").pack(side="left", padx=(0,10))
        tk.Button(top_frame, text="Sobre", command=self.show_about).pack(side="right", padx=10)

        # ---------------- FRAME COM SCROLL ----------------
        container = tk.Frame(root)
        container.pack(fill="both", expand=True)
        canvas = tk.Canvas(container, bg="#f0f4f8")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#f0f4f8")

        # Atualiza área do canvas quando o frame muda de tamanho
        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ---------------- FUNÇÕES ----------------
    def run_search(self):
        """
        Executa a pesquisa usando o ChromaDB quando o usuário clica em 'Pesquisar'.
        """
        consulta = self.query_entry.get().strip()
        top_n = self.top_var.get()
        tipo = self.type_var.get().lower()
        if tipo == "ambos":
            tipo = "both"
        elif tipo == "arquivo":
            tipo = "arquivo"
        elif tipo == "pasta":
            tipo = "pasta"

        # Limpa resultados anteriores
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not consulta:
            messagebox.showwarning("Aviso","Digite algo para pesquisar!")
            return

        resultados = pesquisar_chroma(consulta, top_n, tipo)
        self.display_results(resultados)

    def display_results(self, resultados):
        """
        Exibe os resultados da pesquisa no frame com scroll.
        Cada resultado tem botões para abrir arquivo ou pasta.
        """
        if not resultados:
            tk.Label(self.scroll_frame, text="Nenhum resultado encontrado.", bg="#f0f4f8").pack(pady=5)
            return

        for res in resultados:
            frame = tk.Frame(self.scroll_frame, bg="#e2e8f0", padx=5, pady=5)
            frame.pack(fill="x", pady=2, padx=5)

            # Nome do arquivo/pasta
            tk.Label(frame, text=res.get("nome", "Sem nome"), bg="#e2e8f0", font=("Arial", 10, "bold")).pack(side="left", padx=5)

            # Botão para abrir arquivo
            if res.get("tipo") == "arquivo":
                tk.Button(frame, text="Abrir", command=lambda path=res["caminho"]: abrir_arquivo(path)).pack(side="right", padx=5)

            # Botão para abrir pasta
            tk.Button(frame, text="Pasta", command=lambda path=res["caminho"]: abrir_pasta(path)).pack(side="right", padx=5)

    def show_about(self):
        """
        Exibe informações sobre o aplicativo.
        """
        messagebox.showinfo("Sobre", "Guardian AI FileSearch v1.0\nDesenvolvido por você com ❤️\n2025")

# ---------------- RODAR A APP ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSearchApp(root)
    root.mainloop()
