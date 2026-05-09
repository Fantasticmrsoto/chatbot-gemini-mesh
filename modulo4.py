import json
import os
from modulo1 import NodoBot
from modulo3 import EstadoBot
# ==========================================
# Módulo 4: Persistencia de Datos (JSON)
# ==========================================
class GestorPersistencia:
    def __init__(self, ruta_archivo="mesh_config.json"):
        self.ruta_archivo = ruta_archivo

    def guardar_datos(self, lista_bots):
        """Serializa la Lista Doble, las Colas y las Pilas a un archivo JSON."""
        datos_a_guardar = []
        actual = lista_bots.cabeza

        while actual is not None:
            # 1. Serializar la Cola de Contexto
            mensajes_contexto = []
            nodo_msg = actual.contexto.frente
            while nodo_msg is not None:
                mensajes_contexto.append(nodo_msg.mensaje)
                nodo_msg = nodo_msg.siguiente

            # 2. Serializar la Pila de Historial
            historial_estados = []
            nodo_estado = actual.historial_estados.cima
            while nodo_estado is not None:
                historial_estados.append({
                    "system_instruction": nodo_estado.estado.system_instruction,
                    "temperatura": nodo_estado.estado.temperatura
                })
                nodo_estado = nodo_estado.siguiente

            # 3. Crear diccionario del Bot
            bot_dict = {
                "id": actual.id,
                "nombre": actual.nombre,
                "modelo": actual.modelo,
                "api_key": actual.api_key,
                "system_instruction": actual.system_instruction,
                "contexto": mensajes_contexto,
                "historial": historial_estados
            }
            
            datos_a_guardar.append(bot_dict)
            actual = actual.siguiente

        # Escribir en el archivo JSON
        with open(self.ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos_a_guardar, archivo, indent=4)
        print(f"[Sistema] Datos guardados exitosamente en '{self.ruta_archivo}'.")

    def cargar_datos(self, lista_bots):
        """Deserializa el JSON y reconstruye la Lista Doble, Colas y Pilas en memoria."""
        if not os.path.exists(self.ruta_archivo):
            print(f"[Sistema] Archivo '{self.ruta_archivo}' no encontrado. Iniciando red vacía.")
            return

        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
                datos_cargados = json.load(archivo)

            for bot_data in datos_cargados:
                # 1. Reconstruir el Nodo del Bot principal
                nuevo_bot = NodoBot(
                    bot_data["id"],
                    bot_data["nombre"],
                    bot_data["modelo"],
                    bot_data["api_key"],
                    bot_data["system_instruction"]
                )

                # 2. Reconstruir la Cola de Contexto (FIFO)
                for msg in bot_data.get("contexto", []):
                    nuevo_bot.contexto.encolar(msg)

                # 3. Reconstruir la Pila de Historial (LIFO)
                # Como la pila se guardó desde la cima hacia abajo, debemos 
                # iterar en reversa para que al hacer 'push' la cima original vuelva a quedar arriba.
                historial_guardado = bot_data.get("historial", [])
                for estado_data in reversed(historial_guardado):
                    estado_recuperado = EstadoBot(
                        estado_data["system_instruction"], 
                        estado_data["temperatura"]
                    )
                    nuevo_bot.historial_estados.push(estado_recuperado)

                # 4. Insertar el bot reconstruido en la Lista Doble
                lista_bots.agregar_bot(nuevo_bot)

            print(f"[Sistema] Configuración cargada correctamente ({len(datos_cargados)} bots restaurados).")

        except json.JSONDecodeError:
            print("[Error Crítico] El archivo JSON está corrupto o mal formado.")
        except Exception as e:
            print(f"[Error Crítico] Fallo al cargar datos: {e}")