class NodoMensaje:
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.siguiente = None

class ColaMensajes:
    def __init__(self, limite=10):
        self.frente = None
        self.final_cola = None
        self.limite = limite # N mensajes [cite: 14]
        self.tamano_actual = 0

    def encolar(self, mensaje):
        nuevo_nodo = NodoMensaje(mensaje)
        if self.frente is None:
            self.frente = self.final_cola = nuevo_nodo
        else:
            self.final_cola.siguiente = nuevo_nodo
            self.final_cola = nuevo_nodo
        
        self.tamano_actual += 1
        
        # Desencolar automático si supera la ventana de contexto [cite: 15]
        if self.tamano_actual > self.limite:
            self.desencolar()

    def desencolar(self):
        if self.frente is None:
            return None
        mensaje_eliminado = self.frente.mensaje
        self.frente = self.frente.siguiente
        self.tamano_actual -= 1
        return mensaje_eliminado