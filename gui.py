import tkinter as tk
from tkinter import ttk
from ai_utils import pesquisar_chroma
from file_utils import abrir_arquivo, abrir_pasta

class GuardianApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guardian AI FileSearch")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        # ---------------- Entrada de pesquisa ----------------
        tk.Label(root, text="Digite sua consulta:", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", padx=10, pady=(10,0))
        self.entry = tk.Entry(root, font=("Arial", 12))
        self.entry.pack(fill="x", padx=10, pady=5)
        self.entry.bind("<Return>", lambda event: self.run_search())

        # ---------------- Configurações da pesquisa ----------------
        config_frame = tk.Frame(root, bg="#f0f0f0")
        config_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(config_frame, text="Número de resultados:", bg="#f0f0f0").pack(side="left", padx=5)
        self.top_k_var = tk.IntVar(value=5)
        tk.Spinbox(config_frame, from_=1, to=50, textvariable=self.top_k_var, width=5).pack(side="left", padx=5)

        tk.Label(config_frame, text="Tipo de pesquisa:", bg="#f0f0f0").pack(side="left", padx=5)
        self.tipo_var = tk.StringVar(value="both")
        ttk.Combobox(config_frame, textvariable=self.tipo_var, values=["arquivo", "pasta", "both"], width=10).pack(side="left", padx=5)

        self.btn_search = tk.Button(config_frame, text="Pesquisar", command=self.run_search)
        self.btn_search.pack(side="left", padx=10)

        # ---------------- Frame para resultados com scroll ----------------
        self.frame_container = tk.Frame(root)
        self.frame_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.frame_container, bg="#f0f0f0")
        self.scrollbar = tk.Scrollbar(self.frame_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f0f0")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # ---------------- Executa pesquisa ----------------
    def run_search(self):
        consulta = self.entry.get()
        if not consulta:
            return
        top_k = self.top_k_var.get()
        tipo = self.tipo_var.get()
        resultados = pesquisar_chroma(consulta, top_k=top_k, tipo=tipo)
        self.display_results(resultados, consulta)

    # ---------------- Exibe resultados com highlight e botões ----------------
    def display_results(self, resultados, consulta):
        # Limpa resultados antigos
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for tipo, lista in resultados.items():
            tk.Label(self.scrollable_frame, text=tipo, font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", pady=5)

            for res in lista:
                path = res["path"] if isinstance(res, dict) else str(res)
                snippet = res.get("snippet", "") if isinstance(res, dict) else ""
                score = res.get("score", 0) if isinstance(res, dict) else 0

                # Frame de cada resultado
                frame = tk.Frame(self.scrollable_frame, bg="#e2e8f0", pady=5, padx=5)
                frame.pack(fill="x", padx=5, pady=3)

                # Frame do texto + snippet
                text_frame = tk.Frame(frame, bg="#e2e8f0")
                text_frame.pack(side="left", fill="both", expand=True)

                # Path em negrito
                tk.Label(text_frame, text=path, font=("Arial", 10, "bold"), bg="#e2e8f0").pack(anchor="w")

                # Snippet com highlight
                self.create_highlight(text_frame, snippet, consulta)

                # Frame dos botões
                btn_frame = tk.Frame(frame, bg="#e2e8f0")
                btn_frame.pack(side="right", padx=5)

                tk.Button(btn_frame, text="Abrir Arquivo", command=lambda p=path: abrir_arquivo(p)).pack(pady=2, fill="x")
                tk.Button(btn_frame, text="Abrir Pasta", command=lambda p=path: abrir_pasta(p)).pack(pady=2, fill="x")

                # Score
                tk.Label(frame, text=f"{score:.2f}", bg="#e2e8f0", font=("Arial", 10)).pack(side="right", padx=5)

    # ---------------- Função para highlight ----------------
    def create_highlight(self, parent, texto, consulta):
        parent_text = tk.Text(parent, height=1, bg="#e2e8f0", font=("Arial", 10), borderwidth=0)
        parent_text.pack(fill="x", expand=True)
        parent_text.tag_configure("highlight", foreground="red", font=("Arial", 10, "bold"))

        lower_text = texto.lower()
        lower_query = consulta.lower()
        idx = lower_text.find(lower_query)
        if idx == -1:
            parent_text.insert("1.0", texto)
        else:
            parent_text.insert("1.0", texto[:idx])
            parent_text.insert("end", texto[idx:idx+len(consulta)], "highlight")
            parent_text.insert("end", texto[idx+len(consulta):])
        parent_text.configure(state="disabled")

# ---------------- Execução principal ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = GuardianApp(root)
    root.mainloop()
