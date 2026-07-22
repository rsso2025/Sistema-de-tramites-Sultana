"""Resuelve rutas físicas del sistema para desarrollo y PyInstaller onedir."""

from pathlib import Path
import sys
import tempfile


class PathManager:
    """Centraliza la resolución de rutas del proyecto."""

    @staticmethod
    def is_frozen() -> bool:
        return bool(getattr(sys, "frozen", False))

    @staticmethod
    def get_project_root() -> Path:
        """Raíz del proyecto en modo desarrollo."""
        return Path(__file__).resolve().parents[2]

    @classmethod
    def get_executable_dir(cls) -> Path:
        """Directorio donde reside el ejecutable en modo PyInstaller."""
        if cls.is_frozen():
            return Path(sys.executable).resolve().parent
        return cls.get_project_root()

    @classmethod
    def get_resource_root(cls) -> Path:
        """Base de recursos de solo lectura para desarrollo o bundle PyInstaller."""
        if cls.is_frozen():
            meipass = getattr(sys, "_MEIPASS", None)
            if meipass:
                return Path(meipass).resolve()
            return cls.get_executable_dir()
        return cls.get_project_root()

    @classmethod
    def get_documents_config_path(cls) -> Path:
        return cls.get_resource_root() / "app" / "config" / "documentos_config.json"

    @classmethod
    def get_templates_dir(cls) -> Path:
        return cls.get_resource_root() / "app" / "assets" / "templates"

    @classmethod
    def get_env_path(cls) -> Path:
        return cls.get_executable_dir() / ".env"

    @classmethod
    def get_sqlite_path(cls) -> Path:
        sqlite_path = cls.get_executable_dir() / "app" / "database" / "sistema_tramites.db"
        sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite_path

    @classmethod
    def get_output_dir(cls) -> Path:
        output_dir = cls.get_executable_dir() / "salida_documentos"
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    @classmethod
    def get_temp_dir(cls) -> Path:
        temp_dir = Path(tempfile.gettempdir()) / "SistemaTramitesSultana"
        temp_dir.mkdir(parents=True, exist_ok=True)
        return temp_dir