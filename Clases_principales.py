import json
import os

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class ListaSimple:
    def __init__(self):
        self.cabeza = None
        self.contador = 0

    def agregar(self, publicacion):
        nuevo = Nodo(publicacion)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.contador += 1

    def buscar_por_palabra(self, palabra):
        """Busca publicaciones que contengan la palabra en título o cuerpo"""
        resultados = []
        actual = self.cabeza
        while actual:
            if palabra.lower() in actual.dato.titulo.lower() or palabra.lower() in actual.dato.cuerpo.lower():
                resultados.append(actual.dato)
            actual = actual.siguiente
        return resultados

class ListaCircularDoble:
    def __init__(self):
        self.cabeza = None

    def agregar(self, publicacion):
        nuevo = Nodo(publicacion)
        if not self.cabeza:
            self.cabeza = nuevo
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo
        else:
            ultimo = self.cabeza.anterior
            ultimo.siguiente = nuevo
            nuevo.anterior = ultimo
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo

class GestorArchivos:
    ARCHIVO = "datos_red_social.json"

    def guardar(self, lista_simple):
        datos = []
        actual = lista_simple.cabeza
        while actual:
            datos.append({
                "titulo": actual.dato.titulo,
                "cuerpo": actual.dato.cuerpo,
                "likes": actual.dato.likes
            })
            actual = actual.siguiente
        with open(self.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def cargar(self, lista_simple, lista_circular):
        if not os.path.exists(self.ARCHIVO): return
        with open(self.ARCHIVO, "r", encoding="utf-8") as f:
            from interfaz import Publicacion
            for item in json.load(f):
                p = Publicacion(item["titulo"], item["cuerpo"])
                p.likes = item.get("likes", 0)
                lista_simple.agregar(p)
                lista_circular.agregar(p)
