"""Utilidades para versionar modelos con timestamp."""

from datetime import datetime
from pathlib import Path


def get_version_path(solution_name: str, version: str = "v1") -> str:
    """Genera ruta de versión con formato: solution_name/YYYY-MM-DD_version

    Args:
        solution_name: Nombre de la solución (ej: "HIS-10", "HIS-05")
        version: Versión (default: v1)

    Returns:
        str: Ruta relativa (ej: "HIS-10/2026-06-01_v1")
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    return f"{solution_name}/{date_str}_{version}"


def get_full_model_path(solution_name: str, models_dir: Path = None) -> Path:
    """Retorna ruta completa para guardar modelo.

    Args:
        solution_name: Nombre solución (ej: "HIS-10")
        models_dir: Directorio base de modelos (default: "data/06_models/")

    Returns:
        Path: Ruta completa para guardar modelo
    """
    if models_dir is None:
        models_dir = Path("data") / "06_models"

    version_path = get_version_path(solution_name)
    full_path = models_dir / version_path
    full_path.mkdir(parents=True, exist_ok=True)

    return full_path


def get_model_filename(solution_name: str) -> str:
    """Retorna nombre del archivo modelo.

    Args:
        solution_name: Nombre solución

    Returns:
        str: Nombre archivo (ej: "model_HIS-10.pkl")
    """
    return f"model_{solution_name}.pkl"


def get_metadata_filename() -> str:
    """Retorna nombre del archivo de metadata."""
    return "metadata.json"


def get_metrics_filename() -> str:
    """Retorna nombre del archivo de métricas."""
    return "metrics.json"
