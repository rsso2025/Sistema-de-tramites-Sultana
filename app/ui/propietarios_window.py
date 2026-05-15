"""
Ventana de gestión de propietarios (UI).

Ahora delega toda la lógica de negocio en PropietarioService.
Solo maneja la presentación y los eventos de usuario.
"""

import customtkinter as ctk
from app.services.propietario_service import PropietarioService


class PropietariosWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Gestión de Propietarios")
        self.window.geometry("800x600")
        self.window.grab_set()

        # Inyección del servicio (por ahora directa; en el futuro se podrá pasar)
        self.service = PropietarioService()

        self.setup_ui()
        self.cargar_propietarios()

    def setup_ui(self):
        titulo = ctk.CTkLabel(
            self.window,
            text="Gestión de Propietarios",
            font=("Arial", 22, "bold")
        )
        titulo.pack(pady=20)

        self.entry_documento = self.crear_campo("Documento")
        self.entry_nombre = self.crear_campo("Nombre")
        self.entry_telefono = self.crear_campo("Teléfono")
        self.entry_direccion = self.crear_campo("Dirección")

        frame_botones = ctk.CTkFrame(self.window, fg_color="transparent")
        frame_botones.pack(pady=15)

        btn_guardar = ctk.CTkButton(
            frame_botones,
            text="Guardar",
            command=self.guardar_propietario
        )
        btn_guardar.grid(row=0, column=0, padx=10)

        btn_limpiar = ctk.CTkButton(
            frame_botones,
            text="Limpiar",
            command=self.limpiar_campos
        )
        btn_limpiar.grid(row=0, column=1, padx=10)

        btn_recargar = ctk.CTkButton(
            frame_botones,
            text="Recargar lista",
            command=self.cargar_propietarios
        )
        btn_recargar.grid(row=0, column=2, padx=10)

        btn_cerrar = ctk.CTkButton(
            frame_botones,
            text="Cerrar",
            command=self.window.destroy
        )
        btn_cerrar.grid(row=0, column=3, padx=10)

        self.label_estado = ctk.CTkLabel(
            self.window,
            text="",
            font=("Arial", 14)
        )
        self.label_estado.pack(pady=10)

        subtitulo_lista = ctk.CTkLabel(
            self.window,
            text="Lista de propietarios registrados",
            font=("Arial", 16, "bold")
        )
        subtitulo_lista.pack(pady=(10, 5))

        self.textbox_lista = ctk.CTkTextbox(
            self.window,
            width=720,
            height=220,
            font=("Consolas", 12)
        )
        self.textbox_lista.pack(pady=10, padx=20)

    def crear_campo(self, texto_label):
        frame = ctk.CTkFrame(self.window, fg_color="transparent")
        frame.pack(pady=8)

        label = ctk.CTkLabel(
            frame,
            text=texto_label,
            width=120,
            anchor="w"
        )
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", padx=10)
        return entry

    def guardar_propietario(self):
        """Obtiene datos de los campos y los envía al servicio."""
        documento = self.entry_documento.get()
        nombre = self.entry_nombre.get()
        telefono = self.entry_telefono.get()
        direccion = self.entry_direccion.get()

        exito, mensaje = self.service.crear_propietario(
            documento, nombre, telefono, direccion
        )

        if exito:
            self.label_estado.configure(text=mensaje, text_color="green")
            self.cargar_propietarios()
            self.limpiar_campos()
        else:
            self.label_estado.configure(text=mensaje, text_color="red")

    def cargar_propietarios(self):
        """Pide al servicio los datos formateados y los muestra."""
        try:
            encabezado, separador, filas = self.service.obtener_datos_para_lista()
            self.textbox_lista.delete("1.0", "end")
            self.textbox_lista.insert("end", encabezado)
            self.textbox_lista.insert("end", separador)
            for fila in filas:
                self.textbox_lista.insert("end", fila)
        except Exception as e:
            self.label_estado.configure(
                text=f"Error al cargar propietarios: {str(e)}",
                text_color="red"
            )

    def limpiar_campos(self):
        self.entry_documento.delete(0, "end")
        self.entry_nombre.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.entry_direccion.delete(0, "end")