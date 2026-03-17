import tkinter as tk

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.next = None
        self.prev = None

class ListaCircularDoblementeEnlazada:
    def __init__(self, datos):
        self.cabeza = None
        anterior = None
        
        for d in datos:
            nuevo = Nodo(d)
            if not self.cabeza:
                self.cabeza = nuevo
            if anterior:
                anterior.next = nuevo
                nuevo.prev = anterior
            anterior = nuevo
            
        # El toque de magia: Cerramos el círculo
        anterior.next = self.cabeza
        self.cabeza.prev = anterior
        
class AppCircular(tk.Tk):
    def __init__(self, items):
        super().__init__()
        self.title("Scroll Infinito Estructural")
        self.geometry("300x400")
        self.config(bg="#f0f0f0")

        # Inicializar estructura de datos
        self.lista = ListaCircularDoblementeEnlazada(items)
        self.puntero_superior = self.lista.cabeza
        
        # Cantidad de elementos que caben en pantalla
        self.num_slots = 8
        self.labels = []

        self._crear_interfaz()
        self.actualizar_pantalla()

        # Eventos de scroll (Windows/Linux/MacOS)
        self.bind("<MouseWheel>", self.procesar_scroll) # Windows
        self.bind("<Button-4>", self.procesar_scroll)   # Linux up
        self.bind("<Button-5>", self.procesar_scroll)   # Linux down

    def _crear_interfaz(self):
        titulo = tk.Label(self, text="Scroll Infinito Real", font=("Arial", 14, "bold"), bg="#f0f0f0")
        titulo.pack(pady=10)
        
        container = tk.Frame(self, bg="white", bd=2, relief="groove")
        container.pack(padx=20, pady=10, fill="both", expand=True)

        for _ in range(self.num_slots):
            lbl = tk.Label(container, text="", font=("Segoe UI", 11), bg="white", pady=10)
            lbl.pack(fill="x")
            self.labels.append(lbl)

    def actualizar_pantalla(self):
        """Dibuja los datos partiendo desde el puntero superior"""
        aux = self.puntero_superior
        for lbl in self.labels:
            lbl.config(text=f"📌 {aux.dato}")
            aux = aux.next

    def procesar_scroll(self, event):
        # Detectar dirección (ajuste según OS)
        if event.num == 5 or event.delta < 0: # Hacia abajo
            self.puntero_superior = self.puntero_superior.next
        elif event.num == 4 or event.delta > 0: # Hacia arriba
            self.puntero_superior = self.puntero_superior.prev
        
        self.actualizar_pantalla()

# Ejecución
if __name__ == "__main__":
    data = ["Elemento A", "Elemento B", "Elemento C", "Elemento D", "Elemento E"]
    app = AppCircular(data)
    app.mainloop()