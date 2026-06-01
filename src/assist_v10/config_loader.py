"""Cargador de configuración que detecta entorno local vs Azure."""

import os
from pathlib import Path


def get_catalog_path() -> str:
    """Retorna la ruta del catalog.yml según el entorno.

    Returns:
        str: Ruta a catalog_azure.yml si hay credenciales Azure, sino catalog.yml
    """
    if os.getenv("AZURE_STORAGE_CONNECTION_STRING"):
        return str(Path(__file__).parent.parent.parent / "conf" / "base" / "catalog_azure.yml")
    return str(Path(__file__).parent.parent.parent / "conf" / "base" / "catalog.yml")


def is_azure_environment() -> bool:
    """Verifica si estamos en entorno Azure."""
    return bool(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
