from modulo2 import ColaMensajes
from modulo3 import PilaRestauracion
class NodoBot:
    def __init__(self, id_bot, nombre, modelo, api_key, sys_inst):
        # Datos principales
        self.id = id_bot
        self.nombre = nombre
        self.modelo = modelo
        self.api_key = api_key 
        self.system_instruction = sys_inst
        
        # Punteros a Estructuras Hijas
        self.historial_estados = PilaRestauracion()
        self.contexto = ColaMensajes(limite=10)

        # Punteros de la lista doblemente enlazada
        self.anterior = None
        self.siguiente = None

class ListaDobleBots:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def agregar_bot(self, nuevo_bot):
        """Inserta un nuevo bot al final de la lista doble."""
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo_bot
        else:
            self.cola.siguiente = nuevo_bot
            nuevo_bot.anterior = self.cola
            self.cola = nuevo_bot

    def buscar_bot(self, id_bot):
        """Recorre la lista buscando un bot por su ID."""
        actual = self.cabeza
        while actual:
            if actual.id == id_bot:
                return actual
            actual = actual.siguiente
        return None

    def listar_bots(self):
        """Imprime todos los bots registrados en la red."""
        if self.cabeza is None:
            print("La red de bots está vacía.")
            return
        
        print(f"\n{'ID':<10} | {'NOMBRE':<15} | {'MODELO'}")
        print("-" * 45)
        
        actual = self.cabeza
        while actual:
            print(f"{actual.id:<10} | {actual.nombre:<15} | {actual.modelo}")
            actual = actual.siguiente
        print("-" * 45)

    def eliminar_bot(self, id_bot):
        """Busca y elimina un bot reasignando los punteros de la lista doble."""
        bot_a_eliminar = self.buscar_bot(id_bot)
        
        if bot_a_eliminar is None:
            print(f"Error: No se encontró el bot con ID '{id_bot}'.")
            return False

        # Caso 1: Es el único nodo en la lista
        if self.cabeza == self.cola:
            self.cabeza = None
            self.cola = None
            
        # Caso 2: El nodo a eliminar es la cabeza (el primero)
        elif bot_a_eliminar == self.cabeza:
            self.cabeza = self.cabeza.siguiente
            self.cabeza.anterior = None
            
        # Caso 3: El nodo a eliminar es la cola (el último)
        elif bot_a_eliminar == self.cola:
            self.cola = self.cola.anterior
            self.cola.siguiente = None
            
        # Caso 4: El nodo está en el medio de la lista
        else:
            bot_a_eliminar.anterior.siguiente = bot_a_eliminar.siguiente
            bot_a_eliminar.siguiente.anterior = bot_a_eliminar.anterior

        # Buena práctica: Limpiar los punteros del nodo eliminado
        bot_a_eliminar.siguiente = None
        bot_a_eliminar.anterior = None
        
        print(f"Bot '{bot_a_eliminar.nombre}' eliminado correctamente de la red.")
        return True

    def actualizar_bot(self, id_bot, nuevo_nombre=None, nuevo_modelo=None):
        """Actualiza la información básica de un bot existente."""
        bot = self.buscar_bot(id_bot)
        if bot:
            if nuevo_nombre: 
                bot.nombre = nuevo_nombre
            if nuevo_modelo: 
                bot.modelo = nuevo_modelo
            print(f"Información del bot '{bot.id}' actualizada.")
            return True
            
        print("Bot no encontrado para actualizar.")
        return False