# Clase Principal: Nodo
class Nodo:
    def __init__(self, contenido):
        self.contenido = contenido  # Texto de la publicación 
        self.siguiente = None       # Puntero al siguiente nodo 
        self.anterior = None        # Puntero al anterior 
