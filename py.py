import tkinter as tk
from tkinter import messagebox, font
from Clases_principales import ListaSimple, ListaCircularDoble, GestorArchivos

class Publicacion: 
    def __init__(self, titulo, cuerpo):
        self.titulo = titulo
        self.cuerpo = cuerpo 
        self.likes = 0

class AppNeon(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("URL Social - Edición Neon")
        self.geometry("600x800")
        
        # Colores llamativos
        self.bg_main = "#FFFFFF"   # Gris oscuro
        self.accent_1 = "#16ADAA"  # Cian
        self.accent_2 = "#4375E8"  # Rosa
        self.text_color = "#000000"
        
        self.config(bg=self.bg_main)
        
        # Estructuras [cite: 30, 32, 34]
        self.lista_general = ListaSimple()
        self.lista_feed = ListaCircularDoble()
        self.gestor = GestorArchivos()
        self.modo_circular = False
        
        self.gestor.cargar(self.lista_general, self.lista_feed)
        self.puntero_actual = self.lista_feed.cabeza

        self._crear_interfaz()
        self.actualizar_pantalla()
        self.protocol("WM_DELETE_WINDOW", lambda: [self.gestor.guardar(self.lista_general), self.destroy()])

    def _crear_interfaz(self):
        # Barra de Búsqueda con funcionalidad corregida 
        frame_busq = tk.Frame(self, bg=self.accent_1, padx=2, pady=2)
        frame_busq.pack(fill="x", padx=20, pady=15)
        
        inner_busq = tk.Frame(frame_busq, bg=self.bg_main)
        inner_busq.pack(fill="x")

        self.ent_busqueda = tk.Entry(inner_busq, bg=self.bg_main, fg=self.accent_1, 
                                     insertbackground="white", border=0, font=("Arial", 11))
        self.ent_busqueda.pack(side="left", padx=10, pady=8, expand=True, fill="x")
        
        tk.Button(inner_busq, text="🔍 BUSCAR", bg=self.accent_1, fg=self.bg_main, 
                  font=("Arial", 9, "bold"), command=self.ejecutar_busqueda).pack(side="right")

        # Formulario de Post
        frame_post = tk.Frame(self, bg=self.accent_2, padx=2, pady=2)
        frame_post.pack(fill="x", padx=20, pady=10)
        
        f_body = tk.Frame(frame_post, bg=self.bg_main, padx=15, pady=15)
        f_body.pack(fill="x")

        tk.Label(f_body, text="NUEVO POST", fg=self.accent_2, bg=self.bg_main, font=("Arial", 10, "bold")).pack(anchor="w")
        self.ent_t = tk.Entry(f_body, bg="#3d4446", fg="white", border=0)
        self.ent_t.pack(fill="x", pady=5, ipady=3)
        
        self.txt_c = tk.Text(f_body, bg="#3d4446", fg="white", height=3, border=0)
        self.txt_c.pack(fill="x", pady=5)

        tk.Button(f_body, text="PUBLICAR EN EL FEED", bg=self.accent_2, fg="white", 
                  font=("Arial", 10, "bold"), command=self.publicar).pack(fill="x", pady=5)

        # Visualizador de Publicación
        self.card = tk.Frame(self, bg="#3d4446", padx=25, pady=25)
        self.card.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.lbl_t = tk.Label(self.card, text="", fg=self.accent_1, bg="#3d4446", font=("Arial", 16, "bold"))
        self.lbl_t.pack()
        self.lbl_c = tk.Label(self.card, text="", fg="white", bg="#3d4446", font=("Arial", 12), wraplength=450)
        self.lbl_c.pack(pady=20)
        
        self.btn_like = tk.Button(self.card, text="❤️ 0 LIKES", bg=self.accent_2, fg="white", 
                                  command=self.dar_like)
        self.btn_like.pack()

        # Botones de Navegación [cite: 52, 53]
        nav_f = tk.Frame(self, bg=self.bg_main)
        nav_f.pack(pady=10)
        tk.Button(nav_f, text="◀ ANTERIOR", bg=self.accent_1, command=self.anterior).pack(side="left", padx=20)
        tk.Button(nav_f, text="SIGUIENTE ▶", bg=self.accent_1, command=self.siguiente).pack(side="right", padx=20)

    def ejecutar_busqueda(self):
        """Implementación real de la búsqueda """
        palabra = self.ent_busqueda.get()
        if not palabra: return
        
        resultados = self.lista_general.buscar_por_palabra(palabra)
        if resultados:
            mensaje = f"Se encontraron {len(resultados)} posts:\n\n"
            for r in resultados:
                mensaje += f"• {r.titulo}\n"
            messagebox.showinfo("Resultados", mensaje)
        else:
            messagebox.showinfo("Búsqueda", "No hay coincidencias.")

    def publicar(self):
        t, c = self.ent_t.get(), self.txt_c.get("1.0", "end-1c")
        if t and c:
            p = Publicacion(t, c)
            self.lista_general.agregar(p)
            self.lista_feed.agregar(p)
            if not self.puntero_actual: self.puntero_actual = self.lista_feed.cabeza
            self.actualizar_pantalla()
            self.ent_t.delete(0, tk.END)
            self.txt_c.delete("1.0", tk.END)

    def actualizar_pantalla(self):
        if self.puntero_actual:
            p = self.puntero_actual.dato
            self.lbl_t.config(text=p.titulo.upper())
            self.lbl_c.config(text=p.cuerpo)
            self.btn_like.config(text=f"❤️ {p.likes} LIKES")

    def dar_like(self):
        if self.puntero_actual:
            self.puntero_actual.dato.likes += 1
            self.actualizar_pantalla()

    def siguiente(self):
        if self.puntero_actual:
            if not self.modo_circular and self.puntero_actual.siguiente == self.lista_feed.cabeza:
                messagebox.showinfo("Fin", "Llegaste al final. Activa el modo circular.")
                return
            self.puntero_actual = self.puntero_actual.siguiente
            self.actualizar_pantalla()

    def anterior(self):
        if self.puntero_actual:
            if not self.modo_circular and self.puntero_actual == self.lista_feed.cabeza:
                return
            self.puntero_actual = self.puntero_actual.anterior
            self.actualizar_pantalla()

if __name__ == "__main__":
    AppNeon().mainloop()
