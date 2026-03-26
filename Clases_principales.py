"""
Py sobre las clases principales, aca trabajan las 3 listas principales
"""
import json  # Herramienta para convertir datos en un archivo de texto que la PC entienda
import os    # Herramienta para revisar si el archivo de guardado ya existe en la carpeta

# --- (NODO) ---
class Nodo:
    def __init__(self, dato):
        self.dato = dato        # Aquí guardamos la publicación (título, texto, etc.)
        self.siguiente = None   # Un brazo que apunta al siguiente vagón
        self.anterior = None    # Un brazo que apunta al vagón de atrás (solo para lista doble)

# --- LISTA SIMPLE (EL ALMACÉN) ---
# Solo caminaremos hacia adelante
class ListaSimple:
    def __init__(self):
        self.cabeza = None      # Indica cuál es el primer post de la fila
        self.contador = 0       # Lleva la cuenta de cuántos posts existen

    def agregar(self, publicacion):
        nuevo = Nodo(publicacion) # Creamos el nodo con el post
        if not self.cabeza:       # Si la fila está vacía entonces:
            self.cabeza = nuevo   # Este nuevo post se convierte en el primero
        else:
            actual = self.cabeza
            while actual.siguiente:      # Si no, caminamos hasta el final de la fila
                actual = actual.siguiente
            actual.siguiente = nuevo      # Y enganchamos el nuevo post al final
        self.contador += 1                # Sumamos uno al total

    def buscar_por_palabra(self, palabra):
        """Busca una palabra mágica en todos los posts"""
        resultados = [] # Aquí guardaremos los que coincidan
        actual = self.cabeza
        while actual:
            # Si la palabra está en el título o en el cuerpo (sin importar mayúsculas)
            if palabra.lower() in actual.dato.titulo.lower() or palabra.lower() in actual.dato.cuerpo.lower():
                resultados.append(actual.dato) # Lo anotamos en la lista de resultados
            actual = actual.siguiente # Pasamos al siguiente post
        return resultados

    def obtener_ranking(self):
        """Ordena los posts de más popular a menos popular"""
        posts = []  
        actual = self.cabeza
        while actual:
            posts.append(actual.dato) # Metemos todos los posts en una lista normal
            actual = actual.siguiente
        # Los ordenamos por "likes" de mayor a menor
        return sorted(posts, key=lambda x: x.likes, reverse=True)

    def obtener_estadisticas(self):
        """Calcula el total de interacciones en la red social"""
        t_likes = 0
        t_comentarios = 0
        t_favoritos = 0
        actual = self.cabeza
        while actual:
            t_likes += actual.dato.likes
            t_comentarios += len(actual.dato.comentarios)
            if actual.dato.es_favorito:
                t_favoritos += 1
            actual = actual.siguiente
        return t_likes, t_comentarios, t_favoritos

# --- LISTA DOBLE (NAVEGACIÓN) ---
# Fila con la que podemos caminar de adelante y atras
class ListaDoble:
    def __init__(self):
        self.cabeza = None # El primer post
        self.cola = None   # El último post

    def agregar(self, publicacion):
        nuevo = Nodo(publicacion)
        if not self.cabeza: # Si está vacía
            self.cabeza = nuevo # Es el primero
            self.cola = nuevo   # Y también el último
        else:
            self.cola.siguiente = nuevo # El que era último ahora apunta al nuevo hacia adelante
            nuevo.anterior = self.cola  # El nuevo apunta al viejo último hacia atrás
            self.cola = nuevo           # Ahora el nuevo es oficialmente el último

# --- LISTA CIRCULAR (SCROLL INFINITO) ---
# El ultimo posto esta amarrado al primero (da la vuelta)
class ListaCircular:
    def __init__(self):
        self.cabeza = None

    def agregar(self, publicacion):
        nuevo = Nodo(publicacion)
        if not self.cabeza: # Si es el primero
            self.cabeza = nuevo
            nuevo.siguiente = nuevo # Se apunta a sí mismo para formar el círculo
        else:
            actual = self.cabeza
            # Buscamos el último post (el que apunta de regreso al primero)
            while actual.siguiente != self.cabeza:
                actual = actual.siguiente
            actual.siguiente = nuevo      # El viejo último ahora apunta al nuevo
            nuevo.siguiente = self.cabeza # El nuevo ahora apunta al primero (cierra el anillo)

# --- GESTOR DE ARCHIVOS (MEMORIA) ---
# Esta clase se encarga de guardar y leer el archivo "datos_red_social.json".
class GestorArchivos:
    ARCHIVO = "datos_red_social.json" # Nombre del archivo en tu carpeta

    def guardar(self, lista_simple):
        """Guarda todo lo que hay en la lista simple en el disco duro"""
        datos = []
        actual = lista_simple.cabeza
        while actual:
            # Convertimos cada post en un "diccionario" (formato que JSON entiende)
            datos.append({
                "titulo": actual.dato.titulo,
                "cuerpo": actual.dato.cuerpo,
                "likes": actual.dato.likes,
                "comentarios": actual.dato.comentarios,
                "favorito": actual.dato.es_favorito
            })
            actual = actual.siguiente
        # Escribimos la lista de datos en el archivo físico
        with open(self.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def cargar(self, lista_s, lista_d, lista_c):
        """Lee el archivo guardado y llena las 3 listas al abrir la app"""
        if not os.path.exists(self.ARCHIVO): return # Si no hay archivo, no hace nada
        try:
            with open(self.ARCHIVO, "r", encoding="utf-8") as f:
                # Importamos la clase Publicacion para poder recrear los objetos
                from interfaz import Publicacion 
                for item in json.load(f):
                    # Creamos el objeto con los datos que leímos
                    p = Publicacion(item["titulo"], item["cuerpo"])
                    p.likes = item.get("likes", 0)
                    p.comentarios = item.get("comentarios", [])
                    p.es_favorito = item.get("favorito", False)
                    # Metemos el post en las tres estructuras de datos
                    lista_s.agregar(p)
                    lista_d.agregar(p)
                    lista_c.agregar(p)
        except Exception: pass # Si el archivo está corrupto, la app abre vacía sin trabarse
