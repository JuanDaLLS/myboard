import tkinter as tk
from tkinter import messagebox

class Publicacion: 
    def __init__(self, titulo, cuerpo):
        self.titulo = titulo
        self.cuerpo = cuerpo 
        self.likes = 0

    def __str__(self):
        resumen_cuerpo = (self.cuerpo[:30] + '...') if len(self.cuerpo) > 30 else self.cuerpo
        return f"{self.titulo.upper()}: {resumen_cuerpo} ({self.likes} likes)"

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.next = None
        self.prev = None

class ListaCircularDoblementeEnlazada:
    def __init__(self, datos=None):
        self.cabeza = None
        if not datos: return
        
        anterior = None
        for d in datos:
        
            obj = Publicacion(d, "Sin contenido") if isinstance(d, str) else d
            nuevo = Nodo(obj)
            if not self.cabeza:
                self.cabeza = nuevo
            if anterior:
                anterior.next = nuevo
                nuevo.prev = anterior
            anterior = nuevo
        
        if self.cabeza:
            anterior.next = self.cabeza
            self.cabeza.prev = anterior
    
    def agregar(self, titulo, cuerpo):
        p = Publicacion(titulo, cuerpo)
        nuevo = Nodo(p)
        if not self.cabeza:
            self.cabeza = nuevo
            nuevo.next = nuevo
            nuevo.prev = nuevo
        else:
            ultimo = self.cabeza.prev
            ultimo.next = nuevo
            nuevo.prev = ultimo
            nuevo.next = self.cabeza
            self.cabeza.prev = nuevo

class AppCircular(tk.Tk):
    def __init__(self, items= None):
        super().__init__()
        self.title("Sistema de Publicaciones Circulares")
        self.geometry("700x800")
        self.config(bg="#f4f4f9")

        self.lista = ListaCircularDoblementeEnlazada(items)
        self.puntero_superior = self.lista.cabeza
        
        self.num_slots = 8 
        self.labels = []

        self._crear_interfaz()
        self.actualizar_pantalla()

        
        self.bind("<MouseWheel>", self.procesar_scroll)
        self.bind("<Button-4>", self.procesar_scroll)
        self.bind("<Button-5>", self.procesar_scroll)

    def _crear_interfaz(self):
        
        frame_form = tk.LabelFrame(self, text=" Nueva Publicación ", font=("Arial", 10, "bold"), bg="#f4f4f9", padx=15, pady=15)
        frame_form.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_form, text="Título:", bg="#f4f4f9").pack(anchor="w")
        self.entry_titulo = tk.Entry(frame_form, font=("Arial", 11))
        self.entry_titulo.pack(fill="x", pady=(0, 10))

        tk.Label(frame_form, text="Cuerpo:", bg="#f4f4f9").pack(anchor="w")
        self.text_cuerpo = tk.Text(frame_form, font=("Arial", 10), height=4) 
        self.text_cuerpo.pack(fill="x", pady=(0, 10))

        self.btn_post = tk.Button(frame_form, text="PUBLICAR", bg="#1877F2", fg="white", 
                                  font=("Arial", 10, "bold"), command=self.ejecutar_agregar)
        self.btn_post.pack(fill="x")

        
        tk.Label(self, text=" Feed Infinito (Scroll para navegar) ", font=("Arial", 9, "italic"), bg="#f4f4f9", fg="#666").pack()


        self.container_feed = tk.Frame(self, bg="white", bd=1, relief="solid")
        self.container_feed.pack(padx=20, pady=10, fill="both", expand=True)

        for _ in range(self.num_slots):
            lbl = tk.Label(self.container_feed, text="", font=("Segoe UI", 10), bg="white", 
                           pady=8, anchor="w", justify="left")
            lbl.pack(fill="x", padx=15)
            
            tk.Frame(self.container_feed, bg="#eee", height=1).pack(fill="x", padx=10)
            self.labels.append(lbl)

    def ejecutar_agregar(self):
        t = self.entry_titulo.get()
        c = self.text_cuerpo.get("1.0", "end-1c") 
        
        if t.strip() == "" or c.strip() == "":
            messagebox.showwarning("Campos vacíos", "Por favor, llena ambos campos.")
            return

        self.lista.agregar(t, c)
        
        self.entry_titulo.delete(0, tk.END)
        self.text_cuerpo.delete("1.0", tk.END)
        
        if not self.puntero_superior:
            self.puntero_superior = self.lista.cabeza
            
        self.actualizar_pantalla()
        messagebox.showinfo("Éxito", "¡Publicación añadida al círculo!")

    def actualizar_pantalla(self):
        if not self.puntero_superior: return
        
        aux = self.puntero_superior
        for lbl in self.labels:
            lbl.config(text=str(aux.dato)) 
            aux = aux.next

    def procesar_scroll(self, event):
        if not self.puntero_superior: return
        if event.num == 5 or event.delta < 0: 
            self.puntero_superior = self.puntero_superior.next
        elif event.num == 4 or event.delta > 0:
            self.puntero_superior = self.puntero_superior.prev
        
        self.actualizar_pantalla()

if __name__ == "__main__":
    app = AppCircular()
    app.mainloop()
    