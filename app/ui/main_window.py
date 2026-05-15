import customtkinter as ctk

from app.ui.propietarios_window import PropietariosWindow
from app.ui.vehiculos_window import VehiculosWindow
from app.ui.documentos_window import DocumentosWindow


class MainWindow:
    def __init__(self, app):
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        # Título principal
        titulo = ctk.CTkLabel(
            self.app,
            text="Sistema de Trámites Sultana",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        # Botón Gestión de Propietarios
        btn_propietarios = ctk.CTkButton(
            self.app,
            text="Gestión de Propietarios",
            width=250,
            height=40,
            command=self.abrir_propietarios
        )
        btn_propietarios.pack(pady=10)

        # Botón Gestión de Vehículos
        btn_vehiculos = ctk.CTkButton(
            self.app,
            text="Gestión de Vehículos",
            width=250,
            height=40,
            command=self.abrir_vehiculos
        )
        btn_vehiculos.pack(pady=10)

        # Botón Gestión de Trámites
        # Se deja visible pero deshabilitado hasta implementar esa ventana
        btn_tramites = ctk.CTkButton(
            self.app,
            text="Gestión de Trámites",
            width=250,
            height=40,
            state="disabled"
        )
        btn_tramites.pack(pady=10)

        # Botón Generar Documentos
        btn_documentos = ctk.CTkButton(
            self.app,
            text="Generar Documentos",
            width=250,
            height=40,
            command=self.abrir_documentos
        )
        btn_documentos.pack(pady=10)

        # Botón Salir
        btn_salir = ctk.CTkButton(
            self.app,
            text="Salir",
            width=250,
            height=40,
            command=self.app.destroy
        )
        btn_salir.pack(pady=10)

    def abrir_propietarios(self):
        PropietariosWindow(self.app)

    def abrir_vehiculos(self):
        VehiculosWindow(self.app)

    def abrir_documentos(self):
        DocumentosWindow(self.app)