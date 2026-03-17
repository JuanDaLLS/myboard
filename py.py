import tkinter as tk

class InfiniteScroll(tk.Frame):
    def __init__(self, parent, items):
        super().__init__(parent)
        
        # 1. Triplicamos los items para el efecto visual
        self.items = items * 3
        
        # Configuración del Canvas
        self.canvas = tk.Canvas(self, width=200, height=300)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Llenar la lista
        for item in self.items:
            tk.Label(self.scrollable_frame, text=item, pady=10, font=("Arial", 14)).pack()

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 2. Detectar el scroll para hacer el salto
        self.canvas.bind("<Map>", self.set_initial_scroll) # Centrar al iniciar
        self.canvas.bind("<Motion>", self.check_infinite_scroll)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def set_initial_scroll(self, event):
        # Ir al inicio del segundo bloque (el centro)
        self.canvas.yview_moveto(0.333)

    def check_infinite_scroll(self, event=None):
        top, bottom = self.canvas.yview()
        
        # 3. Si llega muy arriba o muy abajo, saltar al bloque central
        if top <= 0.05:
            self.canvas.yview_moveto(top + 0.333)
        elif bottom >= 0.95:
            self.canvas.yview_moveto(top - 0.333)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.check_infinite_scroll()

# Uso
root = tk.Tk()
root.title("Infinite Scroll Python")
app = InfiniteScroll(root, [f"Elemento {i}" for i in range(1, 11)])
app.pack(padx=20, pady=20)
root.mainloop()