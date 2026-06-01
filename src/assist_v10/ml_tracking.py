"""Configuración de MLflow para Azure ML Studio."""

import os
from datetime import datetime
import mlflow


def setup_mlflow_azure(experiment_prefix: str = "TCA") -> None:
    """Configura MLflow para usar Azure ML como backend.

    Args:
        experiment_prefix: Prefijo para el nombre del experimento
    """
    try:
        # Usar Azure ML como tracking server
        tracking_uri = "azureml://eastus"
        mlflow.set_tracking_uri(tracking_uri)

        # Crear nombre del experimento con fecha
        date_str = datetime.now().strftime("%Y%m%d")
        experiment_name = f"{experiment_prefix}-{date_str}"
        mlflow.set_experiment(experiment_name)

        print(f"✓ MLflow configurado. Experimento: {experiment_name}")
        print(f"  Tracking URI: {tracking_uri}")

    except Exception as e:
        print(f"⚠ MLflow no disponible en Azure ML: {e}")
        print("  Guardando localmente...")
        # Fallback a local
        mlflow.set_tracking_uri("./mlruns")


def setup_mlflow_local() -> None:
    """Configura MLflow para usar storage local (desarrollo)."""
    mlflow.set_tracking_uri("./mlruns")
    date_str = datetime.now().strftime("%Y%m%d")
    experiment_name = f"TCA-LOCAL-{date_str}"
    mlflow.set_experiment(experiment_name)
    print(f"✓ MLflow local: {experiment_name}")


def setup_mlflow(environment: str = "auto") -> None:
    """Setup automático de MLflow según entorno.

    Args:
        environment: 'azure', 'local', o 'auto' (detecta automáticamente)
    """
    if environment == "auto":
        is_azure = bool(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
        environment = "azure" if is_azure else "local"

    if environment == "azure":
        setup_mlflow_azure()
    else:
        setup_mlflow_local()
