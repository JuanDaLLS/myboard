"""
Py para la interfaz grafica
"""

import tkinter as tk  # Importa la herramienta para crear ventanas y botones
from tkinter import messagebox, font  # Importa alertas de mensajes y manejo de letras
# Importa las estructuras de datos y el guardado desde tu archivo externo
from Clases_principales import ListaSimple, ListaDoble, ListaCircular, GestorArchivos

# --- DEFINICIÓN DEL OBJETO PUBLICACIÓN ---
class Publicacion: 
    def __init__(self, titulo, cuerpo):
        self.titulo = titulo  # Guarda el título del post
        self.cuerpo = cuerpo  # Guarda el texto o mensaje
        self.likes = 0        # Todos los posts empiezan con 0 likes
        self.comentarios = [] # Una lista vacía para guardar comentarios futuros
        self.es_favorito = False # Por defecto, no es un post favorito

# --- CLASE PRINCIPAL DE LA VENTANA ---
class AppNeon(tk.Tk):
    def __init__(self):
        super().__init__()  # Inicializa la ventana de Windows/Mac/Linux
        self.title("URL Social - Edición Neon") # Título de la ventana
        self.geometry("400x750") # Tamaño de la ventana (forma de celular)
        
        # --- COLORES ESTILO NEON ---
        self.col_bg_deep = "#BFBFBF"    # Gris oscuro para el fondo de la app
        self.col_bg_card = "#AEAEAE"    # Gris claro para los cuadros de los posts
        self.col_neon_cyan = "#278027"  # Verde neón para resaltar títulos
        self.col_neon_pink = "#143210"  # Verde oscuro para botones
        self.col_text_main = "#000000"  # Texto principal en negro
        self.col_text_sec  = "#000000"  # Texto secundario en negro
        
        self.config(bg=self.col_bg_deep) # Aplicar el color de fondo a la ventana
        
        # --- CONFIGURACIÓN DE FUENTES ---
        self.font_title = font.Font(family="Helvetica Neue", size=14, weight="bold")
        self.font_body = font.Font(family="Helvetica Neue", size=11)
        self.font_ui = font.Font(family="Helvetica Neue", size=10, weight="bold")

        # --- ESTRUCTURAS DE DATOS (El cerebro de la App) ---
        self.lista_general = ListaSimple()    # Para guardar todo linealmente
        self.lista_nav = ListaDoble()         # Para poder ir "Atrás" y "Adelante"
        self.lista_infinito = ListaCircular() # Para que al llegar al final, regrese al inicio
        self.gestor = GestorArchivos()        # Para guardar/cargar datos del disco duro
        
        self.modo_circular = False  # Interruptor para saber si el modo infinito está activo
        self.auto_repro = False     # Variable para futuras funciones automáticas
        
        # Cargar los datos que ya existían en el archivo guardado
        self.gestor.cargar(self.lista_general, self.lista_nav, self.lista_infinito)
        
        # El "puntero" es como un dedo que señala qué post estamos viendo ahora
        self.puntero_actual = self.lista_nav.cabeza

        self._crear_interfaz_estilo_movil() # Llama a la función que dibuja todo
        self.actualizar_pantalla()          # Muestra el primer post en pantalla
        
        # Si el usuario cierra la ventana, se ejecuta la función para guardar datos
        self.protocol("WM_DELETE_WINDOW", self.cerrar_app)

    def _crear_interfaz_estilo_movil(self):
        """Dibuja los elementos visuales en la pantalla"""
        
        # --- 1. BARRA SUPERIOR (Buscador) ---
        frame_top = tk.Frame(self, bg=self.col_bg_deep, pady=10) # Espacio arriba
        frame_top.pack(fill="x", padx=15)
        
        # Caja para escribir la búsqueda
        self.ent_busqueda = tk.Entry(frame_top, bg=self.col_bg_card, fg=self.col_text_main, 
                                     insertbackground="white", font=self.font_body, bd=0)
        self.ent_busqueda.insert(0, "BUSCAR...") # Texto de ejemplo
        self.ent_busqueda.pack(side="left", expand=True, fill="x", ipady=5)
        
        # Botón con icono de lupa
        tk.Button(frame_top, text="🔍", command=self.ejecutar_busqueda, bg=self.col_bg_card, 
                  fg=self.col_neon_cyan, bd=0).pack(side="left", padx=(5,0))

        # --- 2. CONTADOR DE POSTS ---
        self.lbl_count = tk.Label(self, text="Publicaciones Totales: 0", bg=self.col_bg_deep, 
                                  fg=self.col_neon_cyan, font=self.font_title)
        self.lbl_count.pack(pady=(10, 5))

        # --- 3. FORMULARIO PARA CREAR POSTS ---
        f_post = tk.Frame(self, bg=self.col_bg_card, padx=15, pady=15)
        f_post.pack(fill="x", padx=15, pady=10)
        
        tk.Label(f_post, text="Formulario de Post", fg=self.col_text_sec, bg=self.col_bg_card).pack(anchor="w")
        
        self.ent_t = tk.Entry(f_post, bg=self.col_bg_deep, fg=self.col_text_main, bd=0) # Entrada título
        self.ent_t.insert(0, "Título del Post")
        self.ent_t.pack(fill="x", pady=(5, 10), ipady=5)
        
        self.txt_c = tk.Text(f_post, bg=self.col_bg_deep, fg=self.col_text_main, height=3, bd=0) # Entrada cuerpo
        self.txt_c.insert("1.0", "Contenido del Post")
        self.txt_c.pack(fill="x")
        
        # Botón para publicar
        tk.Button(f_post, text="PUBLICAR EN EL FEED", bg=self.col_neon_pink, fg="white", 
                  command=self.publicar, font=self.font_ui, bd=0).pack(pady=(15, 0), fill="x", ipady=5)

        # --- 4. VISUALIZADOR DE LA PUBLICACIÓN (Tarjeta central) ---
        self.card = tk.Frame(self, bg=self.col_bg_card, highlightthickness=2, highlightbackground=self.col_neon_cyan)
        self.card.pack(fill="both", expand=True, padx=15, pady=10)
        
        f_content = tk.Frame(self.card, bg=self.col_bg_card, padx=20, pady=20)
        f_content.pack(fill="both", expand=True)

        self.lbl_t = tk.Label(f_content, text="", fg=self.col_neon_cyan, bg=self.col_bg_card, font=self.font_title)
        self.lbl_t.pack() # Etiqueta para el título del post que estamos viendo
        
        self.lbl_c = tk.Label(f_content, text="", fg=self.col_text_main, bg=self.col_bg_card, font=self.font_body, wraplength=320)
        self.lbl_c.pack(pady=20, expand=True) # Etiqueta para el texto del post
        
        # Panel de botones de interacción (Like y Favorito)
        f_interact = tk.Frame(f_content, bg=self.col_bg_card)
        f_interact.pack(fill="x", side="bottom")
        
        self.lbl_likes = tk.Label(f_interact, text="❤️ 0 LIKES", fg=self.col_text_main, bg=self.col_bg_card)
        self.lbl_likes.pack(side="left")
        
        self.btn_fav = tk.Button(f_interact, text="⭐", command=self.toggle_favorito, bg=self.col_bg_card, bd=0)
        self.btn_fav.pack(side="right", padx=5)
        
        tk.Button(f_interact, text="Me Gusta", command=self.dar_like, bg=self.col_neon_pink, fg="white", bd=0).pack(side="right", padx=5)

        # --- 5. CONTROLES DE NAVEGACIÓN (Abajo) ---
        f_nav_section = tk.Frame(self, bg=self.col_bg_deep, pady=10)
        f_nav_section.pack(fill="x", side="bottom", padx=15)
        
        f_nav_btns = tk.Frame(f_nav_section, bg=self.col_bg_deep)
        f_nav_btns.pack()
        
        # Botones Anterior, Switch y Siguiente
        tk.Button(f_nav_btns, text="◀ ANTERIOR", command=self.anterior).pack(side="left", padx=10)
        
        self.btn_circ = tk.Button(f_nav_btns, text="OFF", command=self.toggle_circular, bg="#444444", fg="white", width=6)
        self.btn_circ.pack(side="left", padx=10)
        
        tk.Button(f_nav_btns, text="SIGUIENTE ▶", command=self.siguiente).pack(side="left", padx=10)
        
        self.lbl_status_circ = tk.Label(f_nav_section, text="ACTIVAR MODO CIRCULAR", bg=self.col_bg_deep)
        self.lbl_status_circ.pack()

    # --- LÓGICA DE FUNCIONAMIENTO ---

    def actualizar_pantalla(self):
        """Actualiza el texto de la tarjeta con la información del post actual"""
        if self.puntero_actual:
            p = self.puntero_actual.dato # Obtener el objeto Publicacion que está en el nodo
            self.lbl_t.config(text=p.titulo.upper())
            self.lbl_c.config(text=p.cuerpo)
            self.lbl_likes.config(text=f"❤️ {p.likes} LIKES")
            self.btn_fav.config(fg="yellow" if p.es_favorito else "white") # Brilla si es favorito
        else:
            self.lbl_t.config(text="FIN DEL FEED")
            self.lbl_c.config(text="No hay publicaciones disponibles.")
            
        # Actualiza el número total de posts creados
        self.lbl_count.config(text=f"Publicaciones Totales: {self.lista_general.contador}")

    def publicar(self):
        """Crea una nueva publicación y la guarda en todas las listas"""
        t, c = self.ent_t.get(), self.txt_c.get("1.0", "end-1c")
        
        # Validar que el usuario no publique los textos por defecto
        if t == "Título del Post": t = "Post Nuevo"
        if c == "Contenido del Post": c = "..."
        
        if t and c:
            p = Publicacion(t, c) # Crea el objeto
            self.lista_general.agregar(p) # Guarda en Lista Simple
            self.lista_nav.agregar(p)     # Guarda en Lista Doble
            self.lista_infinito.agregar(p) # Guarda en Lista Circular
            
            # Si no estábamos viendo nada, ahora apunta al nuevo post
            if not self.puntero_actual:
                self.puntero_actual = self.lista_infinito.cabeza if self.modo_circular else self.lista_nav.cabeza
            
            self.actualizar_pantalla() # Refresca la vista
            
            # Limpiar los campos de texto
            self.ent_t.delete(0, tk.END); self.ent_t.insert(0, "Título del Post")
            self.txt_c.delete("1.0", tk.END); self.txt_c.insert("1.0", "Contenido del Post")
            self.focus() # Quita el teclado/foco de las cajas de texto

    def siguiente(self):
        """Mueve el puntero al siguiente post"""
        if self.puntero_actual:
            # Si estamos en modo normal y no hay más adelante, avisar
            if not self.modo_circular and self.puntero_actual.siguiente is None:
                messagebox.showinfo("Fin", "Llegaste al final del feed.")
                return
            self.puntero_actual = self.puntero_actual.siguiente # Mover el dedo al siguiente nodo
            self.actualizar_pantalla()

    def anterior(self):
        """Mueve el puntero al post de atrás"""
        if self.puntero_actual:
            if self.modo_circular:
                # La lista circular simple solo va en un sentido (hacia adelante)
                messagebox.showwarning("Navegación", "El modo circular solo permite ir hacia adelante.")
            elif self.puntero_actual.anterior:
                # En modo normal, la lista doble sí deja ir atrás
                self.puntero_actual = self.puntero_actual.anterior
                self.actualizar_pantalla()

    def toggle_circular(self):
        """Cambia entre modo de navegación normal e infinito"""
        self.modo_circular = not self.modo_circular
        if self.modo_circular:
            self.btn_circ.config(text="ON", bg="#00E676", fg="black") # Color verde activo
            self.puntero_actual = self.lista_infinito.cabeza # Cambiar a la estructura circular
        else:
            self.btn_circ.config(text="OFF", bg="#444444", fg="white") # Color gris inactivo
            self.puntero_actual = self.lista_nav.cabeza # Regresar a la estructura doble
        self.actualizar_pantalla()

    def ejecutar_busqueda(self):
        """Busca una palabra en todos los títulos guardados"""
        palabra = self.ent_busqueda.get()
        if palabra == "BUSCAR..." or not palabra: return
        
        # Llama al método de búsqueda de la lista simple
        res = self.lista_general.buscar_por_palabra(palabra)
        if res:
            # Crea un texto con todos los títulos encontrados
            msg = f"Encontrados {len(res)} posts:\n\n" + "\n".join([f"• {p.titulo}" for p in res])
            messagebox.showinfo("Resultados", msg)
        else:
            messagebox.showinfo("Búsqueda", "No se encontró nada.")

    def dar_like(self):
        """Suma un corazón al post actual"""
        if self.puntero_actual:
            self.puntero_actual.dato.likes += 1
            self.actualizar_pantalla()

    def toggle_favorito(self):
        """Marca o desmarca el post como favorito"""
        if self.puntero_actual:
            self.puntero_actual.dato.es_favorito = not self.puntero_actual.dato.es_favorito
            self.actualizar_pantalla()

    def cerrar_app(self):
        """Guarda todo en el archivo antes de salir de la aplicación"""
        self.gestor.guardar(self.lista_general)
        self.destroy() # Cierra la ventana definitivamente

# --- INICIO DEL PROGRAMA ---
if __name__ == "__main__":
    # Esto intenta que la ventana se vea nítida en pantallas modernas
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception: pass
    
    app = AppNeon()
    app.mainloop() # Inicia el ciclo infinito de la aplicación
