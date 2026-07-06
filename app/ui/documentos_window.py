"""
Ventana de generación de documentos (UI).

Utiliza DocumentoService para la lógica de negocio y generación.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import unicodedata
import traceback

from app.services.document_service import DocumentoService
from app.services.vehiculo_mysql_service import VehiculoMySQLService


class DocumentosWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Generación de Documentos")
        self.window.geometry("980x720")
        self.window.grab_set()

        # Servicios
        self.documento_service = DocumentoService()
        self.vehiculo_service = VehiculoMySQLService()

        self.vehiculos_map = {}
        self.vehiculos_cache = []
        self.vehiculos_resultados_actuales = []
        self.vehiculo_data = None
        self.entries_edit = {}
        self.vehiculo_seleccionado = None
        self._busqueda_after_id = None

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

        ctk.CTkLabel(frame_seleccion, text="Buscar vehículo:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_busqueda_vehiculo = ctk.CTkEntry(
            frame_seleccion,
            width=450,
            placeholder_text="Escriba placa, interno o propietario...",
        )
        self.entry_busqueda_vehiculo.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.entry_busqueda_vehiculo.bind("<KeyRelease>", self.on_busqueda_vehiculo_change)

        btn_cargar = ctk.CTkButton(
            frame_seleccion,
            text="Cargar datos",
            command=self.cargar_datos_vehiculo,
        )
        btn_cargar.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(frame_seleccion, text="Resultados:").grid(row=2, column=0, padx=10, pady=(6, 10), sticky="nw")

        frame_resultados = ctk.CTkFrame(frame_seleccion)
        frame_resultados.grid(row=2, column=1, columnspan=2, padx=10, pady=(6, 10), sticky="ew")
        frame_resultados.grid_columnconfigure(0, weight=1)

        self.listbox_vehiculos = tk.Listbox(
            frame_resultados,
            height=8,
            activestyle="none",
            exportselection=False,
        )
        self.listbox_vehiculos.grid(row=0, column=0, sticky="nsew")
        self.listbox_vehiculos.bind("<Double-Button-1>", self.on_vehiculo_doble_click)
        self.listbox_vehiculos.bind("<Return>", self.on_vehiculo_enter)
        self.listbox_vehiculos.bind("<<ListboxSelect>>", self.on_vehiculo_select)

        scrollbar_vehiculos = tk.Scrollbar(frame_resultados, orient="vertical", command=self.listbox_vehiculos.yview)
        scrollbar_vehiculos.grid(row=0, column=1, sticky="ns")
        self.listbox_vehiculos.configure(yscrollcommand=scrollbar_vehiculos.set)

        self.label_resultados = ctk.CTkLabel(
            frame_seleccion,
            text="Cargue los vehículos y comience a escribir para filtrar.",
            text_color="gray30",
        )
        self.label_resultados.grid(row=3, column=1, columnspan=2, padx=10, pady=(0, 10), sticky="w")

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

        frame_formato = ctk.CTkFrame(frame_acciones)
        frame_formato.pack(pady=(15, 5))

        ctk.CTkLabel(
            frame_formato,
            text="Formato de salida:",
        ).pack(side="left", padx=(12, 8), pady=12)

        self.combo_formato_salida = ctk.CTkComboBox(
            frame_formato,
            values=["Word (.docx)", "PDF (.pdf)"],
            width=160,
        )
        self.combo_formato_salida.set("Word (.docx)")
        self.combo_formato_salida.pack(side="left", padx=(0, 12), pady=12)

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
        """Carga una sola vez los vehículos y prepara el filtro en memoria."""
        try:
            resultados = self.vehiculo_service.listar_vehiculos()
            self.vehiculos_map.clear()
            self.vehiculos_cache = []

            for fila in resultados:
                vehiculo_id = fila.get("vehiculo_id")
                placa = (fila.get("placa") or "").strip()
                interno = str(fila.get("interno") or "").strip()
                nombre_propietario = (fila.get("nombre_propietario") or "").strip()
                documento_propietario = str(fila.get("documento_propietario") or "").strip()

                parte_interno = f"Interno {interno}" if interno else "Interno N/A"
                etiqueta = f"{placa} - {parte_interno} - {nombre_propietario}".strip()
                if documento_propietario:
                    etiqueta = f"{etiqueta} ({documento_propietario})"

                item = {
                    "vehiculo_id": vehiculo_id,
                    "placa": placa,
                    "interno": interno,
                    "nombre_propietario": nombre_propietario,
                    "documento_propietario": documento_propietario,
                    "etiqueta": etiqueta,
                    "busqueda": self._normalizar_texto(
                        f"{placa} {interno} {nombre_propietario} {documento_propietario}"
                    ),
                }

                self.vehiculos_cache.append(item)
                self.vehiculos_map[etiqueta] = vehiculo_id

            self._actualizar_resultados_vehiculo("")

            if self.vehiculos_cache:
                self.label_resultados.configure(
                    text=f"{len(self.vehiculos_cache)} vehículos cargados. Escriba para filtrar por placa, interno o propietario.",
                    text_color="gray30",
                )
            else:
                self.label_resultados.configure(
                    text="No hay vehículos disponibles.",
                    text_color="gray30",
                )
        except Exception as e:
            traceback.print_exc()
            self.label_estado.configure(
                text=f"Error cargando vehículos: {str(e)}",
                text_color="red",
            )

    def on_busqueda_vehiculo_change(self, _event=None):
        """Dispara un filtrado en memoria mientras el usuario escribe."""
        if self._busqueda_after_id is not None:
            self.window.after_cancel(self._busqueda_after_id)
        self._busqueda_after_id = self.window.after(120, self._aplicar_filtro_vehiculos)

    def _aplicar_filtro_vehiculos(self):
        self._busqueda_after_id = None
        texto_busqueda = self.entry_busqueda_vehiculo.get().strip()
        self._actualizar_resultados_vehiculo(texto_busqueda)

    def _actualizar_resultados_vehiculo(self, texto_busqueda: str):
        """Rellena la lista visible con los vehículos filtrados en memoria."""
        consulta = self._normalizar_texto(texto_busqueda)
        if consulta:
            resultados = [item for item in self.vehiculos_cache if consulta in item["busqueda"]]
        else:
            resultados = self.vehiculos_cache

        self.listbox_vehiculos.delete(0, tk.END)
        for item in resultados:
            self.listbox_vehiculos.insert(tk.END, item["etiqueta"])

        self.vehiculos_resultados_actuales = resultados

        if resultados:
            self.listbox_vehiculos.selection_clear(0, tk.END)
            self.listbox_vehiculos.selection_set(0)
            self.listbox_vehiculos.activate(0)
            self.vehiculo_seleccionado = resultados[0]
            self.label_resultados.configure(
                text=f"Mostrando {len(resultados)} resultado(s). Use clic o Enter para cargar.",
                text_color="gray30",
            )
        else:
            self.vehiculo_seleccionado = None
            self.label_resultados.configure(
                text="Sin coincidencias para la búsqueda actual.",
                text_color="gray30",
            )

    def on_vehiculo_select(self, _event=None):
        """Sincroniza la selección visible con el vehículo activo."""
        seleccion = self.listbox_vehiculos.curselection()
        if not seleccion:
            self.vehiculo_seleccionado = None
            return

        indice = seleccion[0]
        if 0 <= indice < len(self.vehiculos_resultados_actuales):
            self.vehiculo_seleccionado = self.vehiculos_resultados_actuales[indice]

    def on_vehiculo_doble_click(self, _event=None):
        self.cargar_datos_vehiculo()

    def on_vehiculo_enter(self, _event=None):
        self.cargar_datos_vehiculo()

    def _normalizar_texto(self, texto: str) -> str:
        """Normaliza texto para búsquedas insensibles a mayúsculas y acentos."""
        texto = texto or ""
        texto = unicodedata.normalize("NFKD", texto)
        texto = "".join(caracter for caracter in texto if not unicodedata.combining(caracter))
        return texto.lower().strip()

    def cargar_datos_vehiculo(self):
        """Carga los datos automáticos del vehículo seleccionado."""
        seleccion = self.vehiculo_seleccionado
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un vehículo válido.")
            return

        vehiculo_id = seleccion["vehiculo_id"]
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
        formato_salida = self.combo_formato_salida.get().strip()
        es_pdf = formato_salida == "PDF (.pdf)"

        extension = ".pdf" if es_pdf else ".docx"
        nombre_archivo = f"{prefijo}_{self.vehiculo_data.placa}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"

        titulo_dialogo = "Guardar PDF como" if es_pdf else "Guardar documento como"
        tipos_archivo = [("PDF", "*.pdf")] if es_pdf else [("Documentos Word", "*.docx")]

        ruta_guardado = filedialog.asksaveasfilename(
            title=titulo_dialogo,
            defaultextension=extension,
            filetypes=tipos_archivo,
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
            texto_exito = "PDF generado correctamente" if es_pdf else "Documento generado correctamente"
            self.label_estado.configure(
                text=f"{texto_exito}:\n{mensaje}",
                text_color="green",
            )
            messagebox.showinfo("Éxito", f"{texto_exito}:\n{mensaje}")
            return

        self.label_estado.configure(
            text=f"Error: {mensaje}",
            text_color="red",
        )

        if es_pdf:
            if "plantilla" in mensaje.lower() or "tipo de documento" in mensaje.lower():
                messagebox.showerror("Error", f"No se pudo generar el documento Word intermedio:\n{mensaje}")
            else:
                messagebox.showerror("Error", f"No se pudo convertir el documento a PDF:\n{mensaje}")
        else:
            messagebox.showerror("Error", f"No se pudo generar el documento:\n{mensaje}")