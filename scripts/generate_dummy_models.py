"""Genera modelos dummy y los sube a Azure Blob Storage."""

import pickle
import json
import os
from pathlib import Path
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Configurar
models_dir = Path("data/06_models")
models_dir.mkdir(parents=True, exist_ok=True)

print("Generando modelos dummy...")

# 1. HIS-10 Model (No-Show Prediction)
print("  - HIS-10 model")
X_dummy = np.random.randn(100, 20)
y_dummy = np.random.randint(0, 2, 100)
model_his10 = RandomForestClassifier(n_estimators=10, random_state=42)
model_his10.fit(X_dummy, y_dummy)

his10_path = models_dir / "HIS-10" / "2026-06-01_v1"
his10_path.mkdir(parents=True, exist_ok=True)
with open(his10_path / "model.pkl", "wb") as f:
    pickle.dump(model_his10, f)

# Metrics HIS-10
metrics_his10 = {
    "metrics": {
        "roc_auc": 0.92,
        "pr_auc": 0.88,
        "precision": 0.89,
        "recall": 0.85,
        "f1_score": 0.87,
        "accuracy": 0.90
    }
}
with open(his10_path / "metrics.json", "w") as f:
    json.dump(metrics_his10, f, indent=2)

# 2. HIS-05 Model (Wait Time Prediction)
print("  - HIS-05 model")
model_his05 = RandomForestClassifier(n_estimators=10, random_state=42)
model_his05.fit(X_dummy, y_dummy)

his05_path = models_dir / "HIS-05" / "2026-06-01_v1"
his05_path.mkdir(parents=True, exist_ok=True)
with open(his05_path / "model.pkl", "wb") as f:
    pickle.dump(model_his05, f)

# Metrics HIS-05
metrics_his05 = {
    "oof_R2": 0.78,
    "oof_MAE": 45.3,
    "oof_RMSE": 62.1,
    "n_features": 24
}
with open(his05_path / "metrics.json", "w") as f:
    json.dump(metrics_his05, f, indent=2)

print("\n✓ Modelos generados en data/06_models/")
print(f"  - HIS-10/2026-06-01_v1/model.pkl")
print(f"  - HIS-05/2026-06-01_v1/model.pkl")

# 3. Subir a Azure Blob (si hay credenciales)
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if connection_string:
    from azure.storage.blob import BlobClient

    print("\nSubiendo a Azure Blob Storage...")

    # HIS-10
    for file_name in ["model.pkl", "metrics.json"]:
        blob_path = f"models/HIS-10/2026-06-01_v1/{file_name}"
        file_path = his10_path / file_name

        blob_client = BlobClient.from_connection_string(
            connection_string,
            container_name="models",
            blob_name=blob_path
        )
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print(f"  ✓ {blob_path}")

    # HIS-05
    for file_name in ["model.pkl", "metrics.json"]:
        blob_path = f"models/HIS-05/2026-06-01_v1/{file_name}"
        file_path = his05_path / file_name

        blob_client = BlobClient.from_connection_string(
            connection_string,
            container_name="models",
            blob_name=blob_path
        )
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print(f"  ✓ {blob_path}")

    print("\n✓ Modelos subidos a Azure Blob")
else:
    print("\n⚠ AZURE_STORAGE_CONNECTION_STRING no configurada")
    print("  Modelos guardados localmente en data/06_models/")
