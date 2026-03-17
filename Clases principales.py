# Clase Principal: Nodo
class Nodo:
    def __init__(self, contenido):
        self.contenido = contenido  # Texto de la publicación 
        self.siguiente = None       # Puntero al siguiente nodo 
        self.anterior = None        # Puntero al anterior 

# Clase: Lista Enlazada Simple (Almacenamiento General)
class ListaSimple:
    def __init__(self):
        self.cabeza = None
        self.total_publicaciones = 0 # Contador para estadísticas (cuantas publicaciones hay)

    def agregar(self, contenido):
        nuevo_nodo = Nodo(contenido)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.total_publicaciones += 1

    def contar_total(self):
        return self.total_publicaciones # Cumple con el requisito de conteo 
    
# Clase: Lista Doblemente Enlazada (Navegación del Feed)
class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def insertar(self, contenido):
        nuevo_nodo = Nodo(contenido)
        if not self.cabeza:
            self.cabeza = self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo

    def obtener_siguiente(self, nodo_actual):
        return nodo_actual.siguiente if nodo_actual else None

    def obtener_anterior(self, nodo_actual):
        return nodo_actual.anterior if nodo_actual else None
    
# Clase: Lista Circular (Scroll Infinito)
class ListaCircular:
    def __init__(self):
        self.cabeza = None

    def agregar(self, contenido):
        nuevo_nodo = Nodo(contenido)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza # Primer ciclo
        else:
            actual = self.cabeza
            while actual.siguiente != self.cabeza:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza # Cierra el círculo [cite: 33]

    def es_vacia(self):
        return self.cabeza is None
