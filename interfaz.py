"""
Py para la interfaz grafica con Auto-Reproducción y Estadísticas
"""

import tkinter as tk
from tkinter import messagebox, font
from Clases_principales import ListaSimple, ListaDoble, ListaCircular, GestorArchivos

class Publicacion: 
    def __init__(self, titulo, cuerpo):
        self.titulo = titulo
        self.cuerpo = cuerpo
        self.likes = 0
        self.comentarios = []
        self.es_favorito = False

class AppNeon(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("URL Social - Edición Neon")
        self.geometry("400x850") # Ajustado un poco más alto para los nuevos botones
        
        self.col_bg_deep = "#BFBFBF"
        self.col_bg_card = "#AEAEAE"
        self.col_neon_cyan = "#278027"
        self.col_neon_pink = "#143210"
        self.col_text_main = "#000000"
        self.col_text_sec  = "#000000"
        
        self.config(bg=self.col_bg_deep)
        
        self.font_title = font.Font(family="Helvetica Neue", size=14, weight="bold")
        self.font_body = font.Font(family="Helvetica Neue", size=11)
        self.font_ui = font.Font(family="Helvetica Neue", size=10, weight="bold")

        self.lista_general = ListaSimple()
        self.lista_nav = ListaDoble()
        self.lista_infinito = ListaCircular()
        self.gestor = GestorArchivos()
        
        self.modo_circular = False
        self.auto_repro = False  # Controla si el modo automático está encendido
        
        self.gestor.cargar(self.lista_general, self.lista_nav, self.lista_infinito)
        self.puntero_actual = self.lista_nav.cabeza

        self._crear_interfaz_estilo_movil()
        self.actualizar_pantalla()
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)

    def _crear_interfaz_estilo_movil(self):
        # --- 1. BARRA SUPERIOR ---
        frame_top = tk.Frame(self, bg=self.col_bg_deep, pady=10)
        frame_top.pack(fill="x", padx=15)
        
        self.ent_busqueda = tk.Entry(frame_top, bg=self.col_bg_card, fg=self.col_text_main, font=self.font_body, bd=0)
        self.ent_busqueda.insert(0, "BUSCAR...")
        self.ent_busqueda.pack(side="left", expand=True, fill="x", ipady=5)
        
        tk.Button(frame_top, text="🔍", command=self.ejecutar_busqueda, bg=self.col_bg_card, fg=self.col_neon_cyan, bd=0).pack(side="left", padx=(5,0))

        # --- 2. CONTADOR Y ESTADÍSTICAS ---
        f_stats_btns = tk.Frame(self, bg=self.col_bg_deep)
        f_stats_btns.pack(fill="x", padx=15)

        self.lbl_count = tk.Label(f_stats_btns, text="Posts: 0", bg=self.col_bg_deep, fg=self.col_neon_cyan, font=self.font_title)
        self.lbl_count.pack(side="left", pady=10)

        tk.Button(f_stats_btns, text="📊 ESTADÍSTICAS", command=self.ver_estadisticas, bg=self.col_neon_pink, fg="white", font=self.font_ui, bd=0).pack(side="right", padx=5)

        # --- 3. FORMULARIO ---
        f_post = tk.Frame(self, bg=self.col_bg_card, padx=15, pady=15)
        f_post.pack(fill="x", padx=15, pady=10)
        
        self.ent_t = tk.Entry(f_post, bg=self.col_bg_deep, fg=self.col_text_main, bd=0)
        self.ent_t.insert(0, "Título del Post")
        self.ent_t.pack(fill="x", pady=(5, 10), ipady=5)
        
        self.txt_c = tk.Text(f_post, bg=self.col_bg_deep, fg=self.col_text_main, height=3, bd=0)
        self.txt_c.insert("1.0", "Contenido del Post")
        self.txt_c.pack(fill="x")
        
        tk.Button(f_post, text="PUBLICAR", bg=self.col_neon_pink, fg="white", command=self.publicar, font=self.font_ui, bd=0).pack(pady=(10, 0), fill="x", ipady=5)
        tk.Button(f_post, text="VER RANKING", bg=self.col_neon_cyan, fg="white", command=self.ver_ranking, font=self.font_ui, bd=0).pack(pady=(5, 0), fill="x", ipady=5)
        
        # --- 4. TARJETA CENTRAL ---
        self.card = tk.Frame(self, bg=self.col_bg_card, highlightthickness=2, highlightbackground=self.col_neon_cyan)
        self.card.pack(fill="both", expand=True, padx=15, pady=10)
        
        f_content = tk.Frame(self.card, bg=self.col_bg_card, padx=20, pady=20)
        f_content.pack(fill="both", expand=True)

        self.lbl_t = tk.Label(f_content, text="", fg=self.col_neon_cyan, bg=self.col_bg_card, font=self.font_title)
        self.lbl_t.pack()
        
        self.lbl_c = tk.Label(f_content, text="", fg=self.col_text_main, bg=self.col_bg_card, font=self.font_body, wraplength=320)
        self.lbl_c.pack(pady=20, expand=True)
        
        self.lbl_comentarios = tk.Label(f_content, text="", fg=self.col_text_sec, bg=self.col_bg_card, font=self.font_ui, justify="left")
        self.lbl_comentarios.pack(pady=(10, 5), fill="x", anchor="w")

        f_add_comment = tk.Frame(f_content, bg=self.col_bg_card)
        f_add_comment.pack(fill="x", pady=5)
        self.ent_comentario = tk.Entry(f_add_comment, bg=self.col_bg_deep, fg=self.col_text_main, bd=0)
        self.ent_comentario.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 5))
        tk.Button(f_add_comment, text="Enviar", command=self.agregar_comentario, bg=self.col_neon_cyan, fg="white", bd=0).pack(side="right")

        f_interact = tk.Frame(f_content, bg=self.col_bg_card)
        f_interact.pack(fill="x", side="bottom")
        self.lbl_likes = tk.Label(f_interact, text="❤️ 0 LIKES", fg=self.col_text_main, bg=self.col_bg_card)
        self.lbl_likes.pack(side="left")
        self.btn_fav = tk.Button(f_interact, text="⭐", command=self.toggle_favorito, bg=self.col_bg_card, bd=0)
        self.btn_fav.pack(side="right", padx=5)
        tk.Button(f_interact, text="Me Gusta", command=self.dar_like, bg=self.col_neon_pink, fg="white", bd=0).pack(side="right", padx=5)

        # --- 5. CONTROLES DE NAVEGACIÓN Y AUTO ---
        f_nav_section = tk.Frame(self, bg=self.col_bg_deep, pady=10)
        f_nav_section.pack(fill="x", side="bottom", padx=15)
        
        # Botón de Auto Reproducción
        self.btn_auto = tk.Button(f_nav_section, text="REPRODUCCIÓN AUTOMÁTICA: OFF", command=self.toggle_auto, bg="#444444", fg="white", font=self.font_ui, bd=0)
        self.btn_auto.pack(fill="x", pady=5, ipady=5)

        f_nav_btns = tk.Frame(f_nav_section, bg=self.col_bg_deep)
        f_nav_btns.pack()
        
        tk.Button(f_nav_btns, text="◀ ANT", command=self.anterior).pack(side="left", padx=10)
        self.btn_circ = tk.Button(f_nav_btns, text="INF: OFF", command=self.toggle_circular, bg="#444444", fg="white", width=8)
        self.btn_circ.pack(side="left", padx=10)
        tk.Button(f_nav_btns, text="SIG ▶", command=self.siguiente).pack(side="left", padx=10)
        # EXAMEN (TEXT< COMMAND)
        #tk.Button(f_post, text="ACCIÓN", bg=self.col_neon_pink, fg="white",
                #command=self.accion_examen, font=self.font_ui, bd=0).pack(pady=(5,0), fill="x", ipady=5)

    # logicaaa

    def ver_estadisticas(self):
        """Muestra una ventana con los datos globales de la red"""
        likes, comentarios, favs = self.lista_general.obtener_estadisticas()
        msg = f"ESTADÍSTICAS GLOBALES\n\n"
        msg += f"Total de Publicaciones: {self.lista_general.contador}\n"
        msg += f"Total de Likes: {likes} ❤️\n"
        msg += f"Total de Comentarios: {comentarios} 💬\n"
        msg += f"Publicaciones Favoritas: {favs} ⭐"
        messagebox.showinfo("Reporte de Uso", msg)

    def toggle_auto(self):
        """Activa o desactiva el cambio automático cada 2 segundos"""
        self.auto_repro = not self.auto_repro
        if self.auto_repro:
            self.btn_auto.config(text="REPRODUCCIÓN AUTOMÁTICA: ON", bg="#00E676", fg="black")
            # Forzamos modo circular para que no se detenga al final
            if not self.modo_circular: self.toggle_circular()
            self.ciclo_reproduccion()
        else:
            self.btn_auto.config(text="REPRODUCCIÓN AUTOMÁTICA: OFF", bg="#444444", fg="white")

    def ciclo_reproduccion(self):
        """Función que se llama a sí misma cada 2000ms"""
        if self.auto_repro:
            self.siguiente()
            # El número 2000 representa 2 segundos (milisegundos)
            self.after(2000, self.ciclo_reproduccion)

    def actualizar_pantalla(self):
        if self.puntero_actual:
            p = self.puntero_actual.dato 
            self.lbl_t.config(text=p.titulo.upper())
            self.lbl_c.config(text=p.cuerpo)
            self.lbl_likes.config(text=f" {p.likes} LIKES")
            self.btn_fav.config(fg="yellow" if p.es_favorito else "white")
            text_comentarios = "Comentarios:\n" + "\n".join([f"• {c}" for c in p.comentarios[-2:]]) if p.comentarios else "¡Sé el primero en comentar!"
            self.lbl_comentarios.config(text=text_comentarios)
        else:
            self.lbl_t.config(text="FIN DEL FEED")
            self.lbl_c.config(text="No hay publicaciones disponibles.")
        self.lbl_count.config(text=f"Posts: {self.lista_general.contador}")

    def publicar(self):
        t, c = self.ent_t.get(), self.txt_c.get("1.0", "end-1c")
        if t and c:
            p = Publicacion(t, c)
            self.lista_general.agregar(p)
            self.lista_nav.agregar(p)
            self.lista_infinito.agregar(p)
            if not self.puntero_actual:
                self.puntero_actual = self.lista_infinito.cabeza if self.modo_circular else self.lista_nav.cabeza
            self.actualizar_pantalla()
            self.ent_t.delete(0, tk.END); self.txt_c.delete("1.0", tk.END)

    def siguiente(self):
        if self.puntero_actual:
            if not self.modo_circular and self.puntero_actual.siguiente is None:
                if self.auto_repro: self.toggle_auto() # Detener si llega al final en modo normal
                messagebox.showinfo("Fin", "Llegaste al final del feed.")
                return
            self.puntero_actual = self.puntero_actual.siguiente
            self.actualizar_pantalla()

    def anterior(self):
        if self.puntero_actual:
            if self.modo_circular:
                messagebox.showwarning("Navegación", "El modo circular solo va hacia adelante.")
            elif self.puntero_actual.anterior:
                self.puntero_actual = self.puntero_actual.anterior
                self.actualizar_pantalla()

    def toggle_circular(self):
        self.modo_circular = not self.modo_circular
        if self.modo_circular:
            self.btn_circ.config(text="INF: ON", bg="#00E676", fg="black")
            self.puntero_actual = self.lista_infinito.cabeza
        else:
            self.btn_circ.config(text="INF: OFF", bg="#444444", fg="white")
            self.puntero_actual = self.lista_nav.cabeza
        self.actualizar_pantalla()

    def ejecutar_busqueda(self):
        palabra = self.ent_busqueda.get()
        if palabra == "BUSCAR..." or not palabra: return
        res = self.lista_general.buscar_por_palabra(palabra)
        if res:
            msg = f"Encontrados {len(res)} posts:\n\n" + "\n".join([f"• {p.titulo}" for p in res])
            messagebox.showinfo("Resultados", msg)
        else:
            messagebox.showinfo("Búsqueda", "No se encontró nada.")

    def ver_ranking(self):
        ranking = self.lista_general.obtener_ranking()
        if not ranking: return
        msg = "TOP PUBLICACIONES\n\n"
        for i, p in enumerate(ranking[:5], 1):
            msg += f"{i}. {p.titulo} — {p.likes} likes\n"
        messagebox.showinfo("Ranking", msg)
        
    def dar_like(self):
        if self.puntero_actual:
            self.puntero_actual.dato.likes += 1
            self.actualizar_pantalla()
    
    def agregar_comentario(self):
        texto = self.ent_comentario.get()
        if texto.strip() and self.puntero_actual:
            self.puntero_actual.dato.comentarios.append(texto) 
            self.ent_comentario.delete(0, tk.END) 
            self.actualizar_pantalla() 

    def toggle_favorito(self):
        if self.puntero_actual:
            self.puntero_actual.dato.es_favorito = not self.puntero_actual.dato.es_favorito
            self.actualizar_pantalla()

    def accion_examen(self):
        pass

    def cerrar_app(self):
        self.gestor.guardar(self.lista_general)
        self.destroy()

if __name__ == "__main__":
    app = AppNeon()
    app.mainloop()
