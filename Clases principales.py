# Clase Principal: Nodo
class Nodo:
    def __init__(self, texto):
        self.texto = texto        # El mensaje de la publicación
        self.siguiente = None      # Brazo derecho: señala al siguiente
        self.anterior = None       # Brazo izquierdo: señala al anterior (para la Lista Doble)
        self.likes = 0             # Espacio para la función extra de "Me gusta"

# Clase: Lista Enlazada Simple (Almacenamiento General)
class ListaSimple:
    def __init__(self):
        self.cabeza = None         # La primera persona de la fila
        self.contador = 0          # Cuántas personas hay en total

    def agregar_post(self, texto):
        nuevo = Nodo(texto)
        if not self.cabeza:        # Si la fila está vacía, este es el primero
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente: # Caminamos hasta el final de la fila
                actual = actual.siguiente
            actual.siguiente = nuevo # El último ahora señala al nuevo
        self.contador += 1         # Llevamos el registro para el conteo total

    def buscar_por_palabra(self, palabra):
        # Recorre la fila buscando un mensaje específico
        actual = self.cabeza
        while actual:
            if palabra.lower() in actual.texto.lower():
                return f"Encontrado: {actual.texto}"
            actual = actual.siguiente
        return "No se encontró la publicación."

# Clase: Lista Doblemente Enlazada (Navegación del Feed)    
class ListaDoble:
    def __init__(self):
        self.cabeza = None
        self.ultimo = None

    def insertar(self, texto):
        nuevo = Nodo(texto)
        if not self.cabeza:
            self.cabeza = self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo # El último señala al nuevo
            nuevo.anterior = self.ultimo  # El nuevo se agarra del que era último
            self.ultimo = nuevo           # Ahora el nuevo es el final oficial

# Clase: Lista Circular (Scroll Infinito)
class ListaCircular:
    def __init__(self):
        self.cabeza = None

    def agregar_circular(self, texto):
        nuevo = Nodo(texto)
        if not self.cabeza:
            self.cabeza = nuevo
            nuevo.siguiente = self.cabeza # Se señala a sí mismo para cerrar el círculo
        else:
            actual = self.cabeza
            while actual.siguiente != self.cabeza: # Buscamos el final del círculo
                actual = actual.siguiente
            actual.siguiente = nuevo    # El último ahora señala al nuevo
            nuevo.siguiente = self.cabeza # El nuevo se conecta con el principio

    def es_vacia(self):
        return self.cabeza is None
