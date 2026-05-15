import customtkinter as ctk

from app.database.database import init_db
from app.ui.main_window import MainWindow


def main():
    # Inicializar base de datos
    init_db()

    # Configuración global de CustomTkinter
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Crear ventana principal
    app = ctk.CTk()
    app.title("Sistema de Trámites Sultana")
    app.geometry("500x450")
    app.resizable(False, False)

    # Cargar interfaz principal
    MainWindow(app)

    # Ejecutar aplicación
    app.mainloop()


if __name__ == "__main__":
    main()