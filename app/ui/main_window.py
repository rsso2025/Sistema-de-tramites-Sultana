import customtkinter as ctk

from app.config.app_config import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    COMPANY_NAME,
)

from app.services.system_service import SystemService

from app.ui.documentos_window import DocumentosWindow
from app.ui.propietarios_window import PropietariosWindow
from app.ui.vehiculos_window import VehiculosWindow


class MainWindow:
    """Ventana principal del Sistema de Trámites Sultana."""

    def __init__(self, app):
        self.app = app
        self.setup_ui()

    def setup_ui(self):

        # ==========================================================
        # CONFIGURACIÓN GENERAL
        # ==========================================================

        self.app.title(f"{APP_NAME} v{APP_VERSION}")

        # ==========================================================
        # TÍTULO
        # ==========================================================

        titulo = ctk.CTkLabel(
            self.app,
            text=APP_NAME,
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=(20, 5))

        subtitulo = ctk.CTkLabel(
            self.app,
            text=APP_DESCRIPTION,
            font=("Arial", 16)
        )
        subtitulo.pack(pady=(0, 25))

        # ==========================================================
        # BOTONES (OCULTOS PARA FUTURAS VERSIONES)
        # ==========================================================

        self.btn_propietarios = ctk.CTkButton(
            self.app,
            text="Gestión de Propietarios",
            width=250,
            height=40,
            command=self.abrir_propietarios
        )

        self.btn_vehiculos = ctk.CTkButton(
            self.app,
            text="Gestión de Vehículos",
            width=250,
            height=40,
            command=self.abrir_vehiculos
        )

        self.btn_tramites = ctk.CTkButton(
            self.app,
            text="Gestión de Trámites",
            width=250,
            height=40,
            state="disabled"
        )

        # ==========================================================
        # BOTÓN PRINCIPAL
        # ==========================================================

        btn_documentos = ctk.CTkButton(
            self.app,
            text="📄 Abrir Módulo Documental",
            width=280,
            height=45,
            command=self.abrir_documentos
        )
        btn_documentos.pack(pady=15)

        # ==========================================================
        # BOTÓN SALIR
        # ==========================================================

        btn_salir = ctk.CTkButton(
            self.app,
            text="Salir",
            width=280,
            height=45,
            command=self.app.destroy
        )
        btn_salir.pack(pady=10)

        # ==========================================================
        # PIE DE LA APLICACIÓN
        # ==========================================================

        footer_frame = ctk.CTkFrame(
            self.app,
            fg_color="transparent"
        )
        footer_frame.pack(
            side="bottom",
            fill="x",
            pady=15
        )

        self.estado_label = ctk.CTkLabel(
            footer_frame,
            text="🟡 Verificando conexión...",
            text_color="#FFC107", # Amarillo
            font=("Arial",11,"bold")
        )
        
        self.estado_label.pack()

        footer = ctk.CTkLabel(
            footer_frame,
            text=f"Versión {APP_VERSION}\n{COMPANY_NAME}",
            justify="center",
            font=("Arial", 10)
        )
        footer.pack(pady=(5, 0))

        # Verificar conexión al finalizar la construcción de la interfaz
        self.actualizar_estado()

        # ==============================================================
    # ESTADO DEL SISTEMA
    # ==============================================================

    def actualizar_estado(self):
        """Actualiza el estado de la conexión con MySQL."""

        if SystemService.verificar_mysql():
            self.estado_label.configure(
                text="🟢 Base de Datos: Conectada",
                text_color="#198754"   # Verde
            )
        else:
            self.estado_label.configure(
                text="🔴 Base de Datos: Sin conexión",
                text_color="#DC3545"   # Rojo
            )

    # ==============================================================
    # APERTURA DE MÓDULOS
    # ==============================================================

    def abrir_propietarios(self):
        PropietariosWindow(self.app)

    def abrir_vehiculos(self):
        VehiculosWindow(self.app)

    def abrir_documentos(self):
        DocumentosWindow(self.app)