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
        self.entries_edit = {}        # almacena (widget, tipo_control, opciones_extra)
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

        # Bloque campos editables dinámicos (ahora preparado para múltiples tipos)
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

    # ========== FÁBRICA DE CONTROLES EDITABLES ==========
    def _crear_widget_editable(self, parent, tipo_control: str, valor_defecto, opciones=None):
        """
        Fábrica de controles para campos editables.

        Actualmente soporta:
            - 'text'       → CTkEntry (campo de texto simple)
            - 'textarea'   → CTkTextbox (área de texto multilínea)
            - 'combo'      → CTkComboBox (selector desplegable)
            - 'checkbox'   → CTkCheckBox (casilla de verificación)
            - 'date'       → tkcalendar.DateEntry (selector de fecha) con fallback automático

        En futuros sprints se podrán añadir nuevos tipos como:
            - 'readonly'   → campo de solo lectura
            - 'radio'      → grupo de botones de opción
            - 'autocomplete' → entrada con autocompletado

        La incorporación de un nuevo tipo solo requerirá extender este método
        y actualizar _obtener_valor_widget(), sin afectar al resto de la ventana.
        """
        if tipo_control == "textarea":
            # Altura ajustada a 120 para mejor experiencia en relatos extensos
            widget = ctk.CTkTextbox(parent, width=250, height=120)
            if valor_defecto:
                widget.insert("0.0", valor_defecto)
            return widget, tipo_control

        elif tipo_control == "combo":
            # ========== VALIDACIONES DEFENSIVAS ==========
            # Estas validaciones garantizan robustez ante configuraciones incompletas
            # o futuras ampliaciones del JSON sin comprometer la estabilidad.
            if opciones is None:
                opciones = [""]
            elif not isinstance(opciones, list):
                opciones = [""]
            elif len(opciones) == 0:
                opciones = [""]
            # Si valor_defecto es None o no está en opciones, se usará el primer elemento
            widget = ctk.CTkComboBox(parent, values=opciones, width=250)
            if valor_defecto is not None and isinstance(valor_defecto, str) and valor_defecto in opciones:
                widget.set(valor_defecto)
            elif opciones:
                widget.set(opciones[0])
            return widget, tipo_control

        elif tipo_control == "checkbox":
            var = tk.IntVar(value=1 if valor_defecto and str(valor_defecto).lower() in ("1", "true", "si") else 0)
            widget = ctk.CTkCheckBox(parent, text="", variable=var, width=250)
            return widget, tipo_control

        elif tipo_control == "date":
            try:
                from tkcalendar import DateEntry

                # Contenedor puente (tk.Frame) para evitar problemas de anidación con CTk
                contenedor = tk.Frame(parent)

                # Crear DateEntry dentro del contenedor
                date_widget = DateEntry(
                    contenedor,
                    date_pattern="dd/MM/yyyy",
                    width=18
                )
                date_widget.pack(fill="x", expand=True)

                # Valor por defecto (opcional)
                if valor_defecto and isinstance(valor_defecto, str):
                    try:
                        dia, mes, anio = map(int, valor_defecto.split('/'))
                        fecha_parse = datetime(anio, mes, dia)
                        date_widget.set_date(fecha_parse)
                    except Exception:
                        pass  # Si falla, se queda con la fecha actual o vacía

                return contenedor, "date"

            except Exception as e:
                import traceback
                print("=" * 70)
                print("ERROR CREANDO DATEENTRY")
                print("Tipo:", type(e))
                print("Mensaje:", e)
                traceback.print_exc()
                print("=" * 70)

                # FALLBACK: si tkcalendar no está instalado o falla, usar CTkEntry
                widget = ctk.CTkEntry(parent, width=250)
                if valor_defecto:
                    widget.insert(0, valor_defecto)
                return widget, "date_fallback"

        else:  # "text" o cualquier otro (por defecto CTkEntry)
            widget = ctk.CTkEntry(parent, width=250)
            if valor_defecto:
                widget.insert(0, valor_defecto)
            return widget, tipo_control

    def _obtener_valor_widget(self, widget, tipo_control: str) -> str:
        """
        Obtiene el valor del widget según su tipo, garantizando siempre un str.
        """
        if tipo_control == "textarea":
            valor = widget.get("0.0", "end").rstrip("\n")
            return valor
        elif tipo_control == "checkbox":
            # Lectura robusta: widget.get() devuelve el valor de la variable asociada
            # (IntVar o BooleanVar). Se considera truthy si está marcado.
            return "SI" if widget.get() else "NO"
        elif tipo_control == "combo":
            return widget.get()
        elif tipo_control == "date":
            try:
                # El widget es el contenedor tk.Frame, el DateEntry es su primer hijo
                date_entry = widget.winfo_children()[0]
                fecha = date_entry.get_date()
                return fecha.strftime("%d/%m/%Y")
            except Exception:
                # Fallback: si falla, devolver el texto del widget o cadena vacía
                try:
                    return widget.winfo_children()[0].get()
                except:
                    return ""
        elif tipo_control == "date_fallback":
            return widget.get()
        else:  # entry y otros
            return widget.get()

    # ========== ACTUALIZACIÓN DE CAMPOS EDITABLES ==========
    def actualizar_campos_editables(self):
        """
        Limpia y vuelve a crear los campos editables según el tipo seleccionado.
        Ahora soporta distintos tipos de controles definidos en la configuración.
        """
        # Limpiar frame (excepto el título)
        for widget in self.frame_edit.winfo_children():
            if widget != self.label_campos_editables:
                widget.destroy()
        self.entries_edit.clear()

        tipo = self.combo_tipo_documento.get().strip()
        config = self.documento_service.obtener_configuracion_documento(tipo)
        if not config:
            return

        campos_edit = config.get("campos_editables", [])

        # Procesar cada campo (tupla o diccionario)
        for i, item in enumerate(campos_edit, start=1):
            # Soporte para tuplas tradicionales (label, key, valor_defecto)
            if isinstance(item, (list, tuple)):
                if len(item) >= 4:
                    label, key, valor_defecto, tipo_control = item[:4]
                    opciones = item[4] if len(item) > 4 else None
                else:
                    label, key, valor_defecto = item[:3]
                    tipo_control = "text"
                    opciones = None
            else:
                # Soporte futuro para diccionarios con más metadatos
                label = item.get("label", "")
                key = item.get("key", "")
                valor_defecto = item.get("valor_defecto", "")
                tipo_control = item.get("tipo_control", "text")
                opciones = item.get("opciones", None)

            fila = (i - 1) // 2 + 1
            col_base = ((i - 1) % 2) * 2

            # Etiqueta
            ctk.CTkLabel(self.frame_edit, text=f"{label}:").grid(
                row=fila, column=col_base, padx=10, pady=8, sticky="w"
            )

            # Crear widget según tipo
            widget, tipo_real = self._crear_widget_editable(
                self.frame_edit,
                tipo_control,
                valor_defecto,
                opciones
            )

            # Colocar en grilla (con expansión para textarea)
            if tipo_control == "textarea":
                widget.grid(row=fila, column=col_base + 1, padx=10, pady=8, sticky="nsew")
                # Asegurar que la fila se expanda
                self.frame_edit.grid_rowconfigure(fila, weight=1)
                self.frame_edit.grid_columnconfigure(col_base + 1, weight=1)
            else:
                widget.grid(row=fila, column=col_base + 1, padx=10, pady=8, sticky="w")

            # Almacenar widget y su tipo para posterior obtención de valor
            self.entries_edit[key] = (widget, tipo_real)

    # ========== MÉTODOS DE VEHÍCULO (SIN CAMBIOS) ==========
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
        if self._busqueda_after_id is not None:
            self.window.after_cancel(self._busqueda_after_id)
        self._busqueda_after_id = self.window.after(120, self._aplicar_filtro_vehiculos)

    def _aplicar_filtro_vehiculos(self):
        self._busqueda_after_id = None
        texto_busqueda = self.entry_busqueda_vehiculo.get().strip()
        self._actualizar_resultados_vehiculo(texto_busqueda)

    def _actualizar_resultados_vehiculo(self, texto_busqueda: str):
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
        texto = texto or ""
        texto = unicodedata.normalize("NFKD", texto)
        texto = "".join(caracter for caracter in texto if not unicodedata.combining(caracter))
        return texto.lower().strip()

    def cargar_datos_vehiculo(self):
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

    # ========== OBTENCIÓN DE DATOS EDITABLES (UNIVERSAL) ==========
    def obtener_datos_editables(self) -> dict:
        """
        Recoge los valores actuales de los campos editables,
        independientemente del tipo de control.
        """
        resultado = {}
        for key, (widget, tipo_control) in self.entries_edit.items():
            try:
                valor = self._obtener_valor_widget(widget, tipo_control)
                resultado[key] = valor
            except Exception:
                # Fallback: intentar get() genérico
                try:
                    resultado[key] = str(widget.get())
                except:
                    resultado[key] = ""
        return resultado

    # ========== GENERACIÓN DE DOCUMENTO (SIN CAMBIOS) ==========
    def generar_documento_final(self):
        if not self.vehiculo_data:
            messagebox.showwarning("Atención", "Primero debe cargar un vehículo.")
            return

        tipo = self.combo_tipo_documento.get().strip()
        if tipo not in self.documento_service.obtener_tipos_documento():
            messagebox.showwarning("Atención", "Seleccione un tipo de documento válido.")
            return

        datos_editables = self.obtener_datos_editables()

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