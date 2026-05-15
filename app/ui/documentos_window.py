"""
Ventana de generación de documentos (UI).

Utiliza DocumentoService para la lógica de negocio y generación.
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from pathlib import Path
from datetime import datetime

from app.services.document_service import DocumentoService
from app.services.vehiculo_service import VehiculoService


class DocumentosWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Generación de Documentos")
        self.window.geometry("980x720")
        self.window.grab_set()

        # Servicios
        self.documento_service = DocumentoService()
        self.vehiculo_service = VehiculoService()

        self.vehiculos_map = {}
        self.vehiculo_data = None
        self.entries_edit = {}

        self.setup_ui()
        self.cargar_tipos_documento()
        self.cargar_vehiculos()

    def setup_ui(self):
        titulo = ctk.CTkLabel(
            self.window,
            text="Generación de Documentos",
            font=("Arial", 22, "bold"),
        )
        titulo.pack(pady=15)

        self.scroll_frame = ctk.CTkScrollableFrame(self.window, width=920, height=600)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Bloque selección
        frame_seleccion = ctk.CTkFrame(self.scroll_frame)
        frame_seleccion.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_seleccion, text="Tipo de documento:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.combo_tipo_documento = ctk.CTkComboBox(
            frame_seleccion,
            values=[],
            width=250,
            command=self.on_tipo_documento_change,
        )
        self.combo_tipo_documento.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(frame_seleccion, text="Vehículo:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.combo_vehiculos = ctk.CTkComboBox(
            frame_seleccion,
            width=450,
            values=["Cargando vehículos..."],
        )
        self.combo_vehiculos.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        btn_cargar = ctk.CTkButton(
            frame_seleccion,
            text="Cargar datos",
            command=self.cargar_datos_vehiculo,
        )
        btn_cargar.grid(row=1, column=2, padx=10, pady=10)

        # Bloque datos automáticos (siempre igual)
        frame_auto = ctk.CTkFrame(self.scroll_frame)
        frame_auto.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            frame_auto,
            text="Datos automáticos",
            font=("Arial", 18, "bold"),
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")

        campos_auto = [
            ("Nombre propietario", "nombre_propietario"),
            ("Documento", "documento_propietario"),
            ("Placa", "placa"),
            ("Marca", "marca"),
            ("Modelo", "modelo"),
            ("Clase", "clase"),
            ("Fecha afiliación", "fecha_afiliacion"),
            ("Número interno", "numero_interno"),
        ]
        self.entries_auto = {}
        for i, (label, key) in enumerate(campos_auto, start=1):
            fila = (i - 1) // 2 + 1
            col_base = ((i - 1) % 2) * 2
            ctk.CTkLabel(frame_auto, text=f"{label}:").grid(
                row=fila, column=col_base, padx=10, pady=8, sticky="w"
            )
            entry = ctk.CTkEntry(frame_auto, width=250)
            entry.grid(row=fila, column=col_base + 1, padx=10, pady=8, sticky="w")
            entry.configure(state="disabled")
            self.entries_auto[key] = entry

        # Bloque campos editables dinámicos
        self.frame_edit = ctk.CTkFrame(self.scroll_frame)
        self.frame_edit.pack(fill="x", padx=10, pady=10)

        self.label_campos_editables = ctk.CTkLabel(
            self.frame_edit,
            text="Campos editables del documento",
            font=("Arial", 18, "bold"),
        )
        self.label_campos_editables.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")

        # Bloque acciones
        frame_acciones = ctk.CTkFrame(self.scroll_frame)
        frame_acciones.pack(fill="x", padx=10, pady=15)

        btn_generar = ctk.CTkButton(
            frame_acciones,
            text="Generar documento",
            command=self.generar_documento_final,
            width=220,
            height=40,
        )
        btn_generar.pack(pady=15)

        self.label_estado = ctk.CTkLabel(
            frame_acciones,
            text="Seleccione un vehículo y pulse 'Cargar datos'.",
            font=("Arial", 13),
        )
        self.label_estado.pack(pady=5)

    def cargar_tipos_documento(self):
        """Carga los tipos de documento desde el servicio."""
        tipos = self.documento_service.obtener_tipos_documento()
        self.combo_tipo_documento.configure(values=tipos)
        if tipos:
            self.combo_tipo_documento.set(tipos[0])
            self.actualizar_campos_editables()

    def on_tipo_documento_change(self, _valor=None):
        """Evento al cambiar el tipo de documento: regenera los campos editables."""
        self.actualizar_campos_editables()

    def actualizar_campos_editables(self):
        """Limpia y vuelve a crear los campos editables según el tipo seleccionado."""
        for widget in self.frame_edit.winfo_children():
            if widget != self.label_campos_editables:
                widget.destroy()
        self.entries_edit.clear()

        tipo = self.combo_tipo_documento.get().strip()
        config = self.documento_service.obtener_configuracion_documento(tipo)
        if not config:
            return

        campos_edit = config.get("campos_editables", [])
        for i, (label, key, valor_defecto) in enumerate(campos_edit, start=1):
            fila = (i - 1) // 2 + 1
            col_base = ((i - 1) % 2) * 2
            ctk.CTkLabel(self.frame_edit, text=f"{label}:").grid(
                row=fila, column=col_base, padx=10, pady=8, sticky="w"
            )
            entry = ctk.CTkEntry(self.frame_edit, width=250)
            entry.grid(row=fila, column=col_base + 1, padx=10, pady=8, sticky="w")
            # Si es campo de fecha y no tiene valor por defecto, poner fecha actual
            if "fecha" in key.lower() and not valor_defecto:
                entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
            else:
                entry.insert(0, valor_defecto if valor_defecto else "")
            self.entries_edit[key] = entry

    def cargar_vehiculos(self):
        """Carga los vehículos en el combo desde el servicio de vehículos."""
        try:
            conn = __import__("app.database.database", fromlist=["get_connection"]).get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT v.id, v.placa, p.nombre, p.documento
                FROM vehiculos v
                INNER JOIN propietarios p ON v.propietario_id = p.id
                ORDER BY v.placa
                """
            )
            resultados = cursor.fetchall()
            conn.close()
            self.vehiculos_map.clear()
            if resultados:
                valores = []
                for fila in resultados:
                    vehiculo_id, placa, nombre, documento = fila
                    etiqueta = f"{placa} - {nombre} ({documento})"
                    valores.append(etiqueta)
                    self.vehiculos_map[etiqueta] = vehiculo_id
                self.combo_vehiculos.configure(values=valores)
                self.combo_vehiculos.set(valores[0])
            else:
                self.combo_vehiculos.configure(values=["No hay vehículos"])
                self.combo_vehiculos.set("No hay vehículos")
        except Exception as e:
            self.label_estado.configure(
                text=f"Error cargando vehículos: {str(e)}",
                text_color="red",
            )

    def cargar_datos_vehiculo(self):
        """Carga los datos automáticos del vehículo seleccionado."""
        seleccion = self.combo_vehiculos.get()
        if seleccion not in self.vehiculos_map:
            messagebox.showwarning("Atención", "Seleccione un vehículo válido.")
            return

        vehiculo_id = self.vehiculos_map[seleccion]
        try:
            vehiculo = self.documento_service.cargar_datos_vehiculo(vehiculo_id)
            if not vehiculo:
                messagebox.showwarning("Atención", "No se encontraron datos del vehículo.")
                return

            self.vehiculo_data = vehiculo

            # Rellenar campos automáticos
            self._set_entry_auto("nombre_propietario", vehiculo.nombre_propietario)
            self._set_entry_auto("documento_propietario", vehiculo.documento_propietario)
            self._set_entry_auto("placa", vehiculo.placa)
            self._set_entry_auto("marca", vehiculo.marca)
            self._set_entry_auto("modelo", vehiculo.modelo)
            self._set_entry_auto("clase", vehiculo.clase)
            self._set_entry_auto("fecha_afiliacion", vehiculo.fecha_afiliacion)
            self._set_entry_auto("numero_interno", vehiculo.numero_interno)

            self.label_estado.configure(
                text="Datos cargados correctamente. Complete o revise los campos editables.",
                text_color="green",
            )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos:\n{str(e)}")

    def _set_entry_auto(self, key, value):
        entry = self.entries_auto[key]
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, str(value) if value else "")
        entry.configure(state="disabled")

    def obtener_datos_editables(self) -> dict:
        """Recoge los valores actuales de los campos editables."""
        return {key: entry.get() for key, entry in self.entries_edit.items()}

    def generar_documento_final(self):
        """Acción del botón Generar documento."""
        if not self.vehiculo_data:
            messagebox.showwarning("Atención", "Primero debe cargar un vehículo.")
            return

        tipo = self.combo_tipo_documento.get().strip()
        if tipo not in self.documento_service.obtener_tipos_documento():
            messagebox.showwarning("Atención", "Seleccione un tipo de documento válido.")
            return

        datos_editables = self.obtener_datos_editables()

        # Nombre sugerido para el archivo
        config = self.documento_service.obtener_configuracion_documento(tipo)
        prefijo = config["nombre_archivo"]
        nombre_archivo = f"{prefijo}_{self.vehiculo_data.placa}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"

        ruta_guardado = filedialog.asksaveasfilename(
            title="Guardar documento como",
            defaultextension=".docx",
            filetypes=[("Documentos Word", "*.docx")],
            initialfile=nombre_archivo,
        )
        if not ruta_guardado:
            self.label_estado.configure(
                text="Generación cancelada por el usuario.",
                text_color="orange",
            )
            return

        exito, mensaje = self.documento_service.generar_documento(
            tipo=tipo,
            vehiculo=self.vehiculo_data,
            datos_editables=datos_editables,
            ruta_salida=ruta_guardado,
        )

        if exito:
            self.label_estado.configure(
                text=f"Documento generado correctamente:\n{mensaje}",
                text_color="green",
            )
            messagebox.showinfo("Éxito", f"Documento generado correctamente:\n{mensaje}")
        else:
            self.label_estado.configure(
                text=f"Error: {mensaje}",
                text_color="red",
            )
            messagebox.showerror("Error", f"No se pudo generar el documento:\n{mensaje}")