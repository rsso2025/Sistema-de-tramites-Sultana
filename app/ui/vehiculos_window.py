"""
Ventana de gestión de vehículos (UI).

Ahora delega toda la lógica en VehiculoService.
"""

import customtkinter as ctk
from app.services.vehiculo_service import VehiculoService


class VehiculosWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Gestión de Vehículos")
        self.window.geometry("950x680")
        self.window.grab_set()

        # Servicio inyectado
        self.service = VehiculoService()
        self.propietarios_map = {}

        self.setup_ui()
        self.cargar_propietarios()
        self.cargar_vehiculos()

    def setup_ui(self):
        titulo = ctk.CTkLabel(
            self.window,
            text="Gestión de Vehículos",
            font=("Arial", 22, "bold")
        )
        titulo.pack(pady=20)

        # Selector de propietario
        frame_propietario = ctk.CTkFrame(self.window, fg_color="transparent")
        frame_propietario.pack(pady=8)
        label_propietario = ctk.CTkLabel(
            frame_propietario,
            text="Propietario",
            width=120,
            anchor="w"
        )
        label_propietario.pack(side="left", padx=10)
        self.combo_propietario = ctk.CTkComboBox(
            frame_propietario,
            width=420,
            values=["Cargando propietarios..."]
        )
        self.combo_propietario.pack(side="left", padx=10)

        self.entry_placa = self.crear_campo("Placa")
        self.entry_numero_interno = self.crear_campo("Número interno")
        self.entry_marca = self.crear_campo("Marca")
        self.entry_modelo = self.crear_campo("Modelo")
        self.entry_clase = self.crear_campo("Clase")
        self.entry_fecha_afiliacion = self.crear_campo("Fecha afiliación")

        frame_botones = ctk.CTkFrame(self.window, fg_color="transparent")
        frame_botones.pack(pady=15)

        ctk.CTkButton(
            frame_botones,
            text="Guardar",
            command=self.guardar_vehiculo
        ).grid(row=0, column=0, padx=10)
        ctk.CTkButton(
            frame_botones,
            text="Limpiar",
            command=self.limpiar_campos
        ).grid(row=0, column=1, padx=10)
        ctk.CTkButton(
            frame_botones,
            text="Recargar lista",
            command=self.recargar_todo
        ).grid(row=0, column=2, padx=10)
        ctk.CTkButton(
            frame_botones,
            text="Cerrar",
            command=self.window.destroy
        ).grid(row=0, column=3, padx=10)

        self.label_estado = ctk.CTkLabel(
            self.window,
            text="",
            font=("Arial", 14)
        )
        self.label_estado.pack(pady=10)

        subtitulo_lista = ctk.CTkLabel(
            self.window,
            text="Lista de vehículos registrados",
            font=("Arial", 16, "bold")
        )
        subtitulo_lista.pack(pady=(10, 5))

        self.textbox_lista = ctk.CTkTextbox(
            self.window,
            width=860,
            height=250,
            font=("Consolas", 12)
        )
        self.textbox_lista.pack(pady=10, padx=20)

    def crear_campo(self, texto_label):
        frame = ctk.CTkFrame(self.window, fg_color="transparent")
        frame.pack(pady=8)
        ctk.CTkLabel(
            frame,
            text=texto_label,
            width=120,
            anchor="w"
        ).pack(side="left", padx=10)
        entry = ctk.CTkEntry(frame, width=420)
        entry.pack(side="left", padx=10)
        return entry

    def cargar_propietarios(self):
        """Carga los propietarios en el combo desde el servicio."""
        try:
            etiquetas, mapa = self.service.obtener_propietarios_para_combo()
            self.propietarios_map = mapa
            self.combo_propietario.configure(values=etiquetas)
            if etiquetas and etiquetas[0] != "No hay propietarios":
                self.combo_propietario.set(etiquetas[0])
            else:
                self.combo_propietario.set("No hay propietarios")
        except Exception as e:
            self.label_estado.configure(
                text=f"Error al cargar propietarios: {str(e)}",
                text_color="red"
            )

    def guardar_vehiculo(self):
        """Recoge datos de la UI y los envía al servicio."""
        propietario_label = self.combo_propietario.get()
        propietario_id = self.propietarios_map.get(propietario_label)
        if not propietario_id:
            self.label_estado.configure(
                text="Seleccione un propietario válido.",
                text_color="red"
            )
            return

        placa = self.entry_placa.get()
        numero_interno = self.entry_numero_interno.get()
        marca = self.entry_marca.get()
        modelo = self.entry_modelo.get()
        clase = self.entry_clase.get()
        fecha_afiliacion = self.entry_fecha_afiliacion.get()

        exito, mensaje = self.service.crear_vehiculo(
            placa=placa,
            numero_interno=numero_interno,
            marca=marca,
            modelo=modelo,
            clase=clase,
            fecha_afiliacion=fecha_afiliacion,
            propietario_id=propietario_id,
        )

        if exito:
            self.label_estado.configure(text=mensaje, text_color="green")
            self.cargar_vehiculos()
            self.limpiar_campos()
        else:
            self.label_estado.configure(text=mensaje, text_color="red")

    def cargar_vehiculos(self):
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
                text=f"Error al cargar vehículos: {str(e)}",
                text_color="red"
            )

    def limpiar_campos(self):
        self.entry_placa.delete(0, "end")
        self.entry_numero_interno.delete(0, "end")
        self.entry_marca.delete(0, "end")
        self.entry_modelo.delete(0, "end")
        self.entry_clase.delete(0, "end")
        self.entry_fecha_afiliacion.delete(0, "end")

    def recargar_todo(self):
        self.cargar_propietarios()
        self.cargar_vehiculos()
        self.label_estado.configure(text="")