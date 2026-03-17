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
