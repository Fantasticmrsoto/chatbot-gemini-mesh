import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Importación de tus módulos
from modulo1 import ListaDobleBots, NodoBot
from modulo3 import EstadoBot
from modulo4 import GestorPersistencia
from modulo5 import LogErrores

# =======================================================
# OPCIÓN A: CLI (Mantenida según tu estructura)
# =======================================================
def lanzar_cli(red, auditoria, persistencia):
    bot_actual = None
    print("\n" + "="*75)
    print("      SISTEMA GEMINI MESH - MODO CONSOLA")
    print("="*75)
    print(f"{'COMANDO':<15} | {'SINTAXIS':<25} | {'DESCRIPCIÓN'}")
    print("-"*75)
    print(f"{'Listar Bots':<15} | {'list':<25} | {'Muestra ID, Nombre y Modelo'}")
    print(f"{'Seleccionar':<15} | {'select <id>':<25} | {'Establece el bot como Actual'}")
    print(f"{'Enviar Mensaje':<15} | {'chat \"<msj>\"':<25} | {'Encola mensaje en la Cola'}")
    print(f"{'Modificar':<15} | {'edit <f> <v>':<25} | {'Cambia datos (Usa Pila)'}")
    print(f"{'Eliminar':<15} | {'delete <id>':<25} | {'Elimina bot de la Lista Doble'}")
    print(f"{'Deshacer':<15} | {'undo':<25} | {'Pop de Pila (Restaura estado)'}")
    print(f"{'Ver Contexto':<15} | {'current':<25} | {'Muestra datos y Cola de chat'}")
    print(f"{'Ver Errores':<15} | {'log':<25} | {'Muestra Lista de Errores'}")
    print(f"{'Salir Bot':<15} | {'exit-chatbot':<25} | {'Deselecciona el bot actual'}")
    print(f"{'Salir Sistema':<15} | {'exit':<25} | {'Guarda JSON y cierra todo'}")
    print("="*75)

    while True:
        status = f"[{bot_actual.nombre}]" if bot_actual else "[SISTEMA]"
        entrada = input(f"{status}_CLI> ").strip()
        if not entrada: continue
        partes = entrada.split(" ", 2)
        comando = partes[0].lower()

        try:
            if comando == "list":
                red.listar_bots()
            elif comando == "select":
                if len(partes) < 2: print("Sintaxis: select <id>")
                else:
                    bot_actual = red.buscar_bot(partes[1])
                    print(f"Seleccionado: {bot_actual.nombre}" if bot_actual else "No encontrado")
            elif comando == "chat":
                if bot_actual:
                    msj = partes[1].replace('"', '')
                    bot_actual.contexto.encolar(msj)
                    print("Mensaje encolado.")
            elif comando == "undo":
                if bot_actual:
                    p = bot_actual.historial_estados.pop()
                    if p: bot_actual.system_instruction = p.system_instruction; print("Estado restaurado.")
            elif comando == "menu": return
            elif comando == "exit":
                persistencia.guardar_datos(red)
                sys.exit(0)
            else: print("Comando no reconocido.")
        except Exception as e:
            print(f"Error: {e}")

# ==========================================
# OPCIÓN B: GUI MEJORADA (ESTILO MODERNO)
# ==========================================
class GeminiMeshGUI:
    def __init__(self, root, red, auditoria, persistencia):
        self.root = root
        self.red = red
        self.auditoria = auditoria
        self.persistencia = persistencia
        self.bot_actual = None
        
        # Configuración de ventana
        self.root.title("GEMINI MESH - IA Manager")
        self.root.geometry("1000x650")
        self.root.configure(bg="#1e1e1e") # Fondo oscuro
        
        self.setup_styles()
        self.setup_ui()
        self.refrescar_lista()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#252526", foreground="white", fieldbackground="#252526", borderwidth=0)
        style.map("Treeview", background=[('selected', '#37373d')])

    def setup_ui(self):
        # --- SIDEBAR (IZQUIERDA) ---
        self.sidebar = tk.Frame(self.root, width=250, bg="#252526", padx=10, pady=10)
        self.sidebar.pack(side="left", fill="y")
        
        tk.Label(self.sidebar, text="CHATBOTS", fg="#007acc", bg="#252526", font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        self.lb_bots = tk.Listbox(self.sidebar, bg="#1e1e1e", fg="#cccccc", borderwidth=0, 
                                  highlightthickness=1, highlightcolor="#007acc", font=("Segoe UI", 10))
        self.lb_bots.pack(fill="both", expand=True, pady=5)
        self.lb_bots.bind('<<ListboxSelect>>', self.seleccionar_bot)
        
        tk.Button(self.sidebar, text="🗑 Eliminar Bot", command=self.gui_eliminar, 
                  bg="#4e1a1a", fg="white", relief="flat", pady=5).pack(fill="x", pady=5)

        # --- CONTENIDO PRINCIPAL (DERECHA) ---
        self.main_f = tk.Frame(self.root, bg="#1e1e1e", padx=20, pady=20)
        self.main_f.pack(side="right", fill="both", expand=True)

        # Cabecera
        self.lbl_titulo = tk.Label(self.main_f, text="Seleccione un bot para comenzar", 
                                   fg="white", bg="#1e1e1e", font=("Segoe UI", 16, "bold"))
        self.lbl_titulo.pack(anchor="w")

        # Pantalla de Chat
        self.txt_display = tk.Text(self.main_f, state="disabled", bg="#2d2d2d", fg="#e1e1e1", 
                                   font=("Consolas", 11), relief="flat", padx=10, pady=10)
        self.txt_display.pack(fill="both", expand=True, pady=15)

        # Panel de Botones de Acción
        btn_f = tk.Frame(self.main_f, bg="#1e1e1e")
        btn_f.pack(fill="x")
        
        btn_style = {"relief": "flat", "padx": 15, "pady": 8, "font": ("Segoe UI", 9, "bold")}
        
        tk.Button(btn_f, text="💬 Enviar Mensaje", command=self.gui_chat, 
                  bg="#007acc", fg="white", **btn_style).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="↺ Deshacer (Pila)", command=self.gui_undo, 
                  bg="#3e3e3e", fg="white", **btn_style).pack(side="left", padx=5)
        
        tk.Button(btn_f, text="💾 Guardar Cambios", command=lambda: self.persistencia.guardar_datos(self.red), 
                  bg="#2d5a27", fg="white", **btn_style).pack(side="right", padx=5)

    def refrescar_lista(self):
        self.lb_bots.delete(0, tk.END)
        c = self.red.cabeza
        while c:
            self.lb_bots.insert(tk.END, f"{c.id}: {c.nombre}")
            c = c.siguiente

    def seleccionar_bot(self, event):
        idx = self.lb_bots.curselection()
        if idx:
            id_b = self.lb_bots.get(idx).split(":")[0]
            self.bot_actual = self.red.buscar_bot(id_b)
            self.lbl_titulo.config(text=f"Bot: {self.bot_actual.nombre} ({self.bot_actual.modelo})")
            self.refrescar_chat()

    def refrescar_chat(self):
        self.txt_display.config(state="normal")
        self.txt_display.delete("1.0", tk.END)
        m = self.bot_actual.contexto.frente
        while m:
            self.txt_display.insert(tk.END, f" USUARIO >> ", "user_tag")
            self.txt_display.insert(tk.END, f"{m.mensaje}\n\n")
            m = m.siguiente
        self.txt_display.tag_config("user_tag", foreground="#569cd6", font=("Consolas", 11, "bold"))
        self.txt_display.config(state="disabled")
        self.txt_display.see(tk.END)

    def gui_chat(self):
        if not self.bot_actual:
            messagebox.showwarning("Atención", "Seleccione un bot de la lista izquierda.")
            return
        m = simpledialog.askstring("Nuevo Mensaje", "Escriba su mensaje:")
        if m: 
            self.bot_actual.contexto.encolar(m)
            self.refrescar_chat()

    def gui_undo(self):
        if self.bot_actual:
            p = self.bot_actual.historial_estados.pop()
            if p: 
                self.bot_actual.system_instruction = p.system_instruction
                self.refrescar_chat()
                messagebox.showinfo("Pila", "Configuración de System Instruction restaurada.")
            else:
                messagebox.showwarning("Pila", "No hay estados previos en la pila.")

    def gui_eliminar(self):
        if self.bot_actual:
            if messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente a {self.bot_actual.nombre}?"):
                self.red.eliminar_bot(self.bot_actual.id)
                self.bot_actual = None
                self.lbl_titulo.config(text="Seleccione un bot")
                self.refrescar_lista()
                self.txt_display.config(state="normal")
                self.txt_display.delete("1.0", tk.END)
                self.txt_display.config(state="disabled")

# ==========================================
# MAIN DRIVER
# ==========================================
if __name__ == "__main__":
    # Inicialización única
    mi_red = ListaDobleBots()
    mis_logs = LogErrores()
    mi_persistencia = GestorPersistencia()
    mi_persistencia.cargar_datos(mi_red)

    while True:
        print("\n" + "="*35)
        print("    GEMINI MESH - MENÚ PRINCIPAL")
        print("="*35)
        print(" 1. Iniciar Interfaz de Consola (A)")
        print(" 2. Iniciar Interfaz Gráfica (B)")
        print(" 3. Salir y Guardar Todo")
        print("="*35)
        
        op = input("Seleccione una opción: ")
        
        if op == "1":
            lanzar_cli(mi_red, mis_logs, mi_persistencia)
        elif op == "2":
            root = tk.Tk()
            gui = GeminiMeshGUI(root, mi_red, mis_logs, mi_persistencia)
            root.mainloop()
        elif op == "3":
            mi_persistencia.guardar_datos(mi_red)
            print("Datos guardados. Saliendo...")
            break
        else:
            print("Opción no válida.")