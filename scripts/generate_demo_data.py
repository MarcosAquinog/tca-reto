"""Genera datos dummy realistas para demo."""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Configurar seed para reproducibilidad
np.random.seed(42)

# Crear directorio
data_dir = Path("data/01_raw")
data_dir.mkdir(parents=True, exist_ok=True)

print("Generando datos dummy para demo...")

# 1. HOSPAC - Información de pacientes
print("  - hospac.parquet")
n_pacientes = 5000
hospac = pd.DataFrame({
    "m_num_exp": [f"EXP{i:07d}" for i in range(n_pacientes)],
    "p_sexo": np.random.choice(["M", "F"], n_pacientes),
    "p_edad": np.random.randint(18, 85, n_pacientes),
    "p_tpo_pac": np.random.choice(["H", "A"], n_pacientes),
    "m_ciu": np.random.choice(["001", "002", "003", "004", "005"], n_pacientes),
    "m_col": np.random.choice(["0001", "0002", "0003", "0004"], n_pacientes),
    "m_cp": np.random.choice(["28001", "28002", "28003", "28004", "28005"], n_pacientes),
    "m_edo": np.random.choice(["01", "02", "03", "04", "05"], n_pacientes),
    "m_pai": np.random.choice(["MEX", "USA", "OTR"], n_pacientes),
})
hospac.to_parquet(data_dir / "hospac.parquet", index=False)

# 2. HOSAGD - Citas programadas
print("  - hosagd.parquet")
n_citas = 10000
base_date = datetime(2024, 1, 1)
hosagd = pd.DataFrame({
    "m_num_exp": np.random.choice(hospac["m_num_exp"], n_citas),
    "med": [f"{i:06d}" for i in np.random.randint(1, 999, n_citas)],
    "esp": np.random.choice(["Cardiología", "Dermatología", "Neurología", "Oncología", "Pediatría"], n_citas),
    "a_fecha": [base_date + timedelta(days=int(d)) for d in np.random.uniform(0, 90, n_citas)],
    "hra_ini": [f"{h:02d}:{m:02d}" for h, m in zip(np.random.randint(8, 17, n_citas), np.random.randint(0, 60, n_citas))],
    "buffer": np.random.choice(["N", "S"], n_citas),
    "tpo_cita": np.random.choice(["P", "U", "S"], n_citas),
    "duration_min": np.random.randint(15, 60, n_citas),
    "lead_time_days": np.random.randint(1, 30, n_citas),
    "area": np.random.choice(["Consulta Externa", "Emergencias", "Urgencias", "Triage"], n_citas),
    "conflicto": np.random.choice(["C", "N"], n_citas),
    "agregada": np.random.choice(["A", "N"], n_citas),
    "ultimahora": np.random.choice(["U", "N"], n_citas),
    "no_show": np.random.choice([0, 1], n_citas, p=[0.85, 0.15]),  # 15% no-shows
})
hosagd.to_parquet(data_dir / "hosagd.parquet", index=False)

# 3. HOSMPI - Índice maestro de pacientes
print("  - hosmpi.parquet")
hosmpi = pd.DataFrame({
    "m_num_exp": hospac["m_num_exp"],
    "p_status": np.random.choice(["A", "I"], len(hospac)),
})
hosmpi.to_parquet(data_dir / "hosmpi.parquet", index=False)

# 4. TRIAGE - Registros de triaje
print("  - triage.parquet")
n_triage = 15000
triage = pd.DataFrame({
    "m_num_exp": np.random.choice(hospac["m_num_exp"], n_triage),
    "triage_nivel": np.random.choice([1, 2, 3, 4, 5], n_triage),
    "timestamp": [base_date + timedelta(hours=int(h)) for h in np.random.uniform(0, 2160, n_triage)],
})
triage.to_parquet(data_dir / "triage.parquet", index=False)

# 5. NOTAMEDICAURG - Notas médicas de urgencia
print("  - notamedicaurg.parquet")
n_notas = 8000
notamedicaurg = pd.DataFrame({
    "m_num_exp": np.random.choice(hospac["m_num_exp"], n_notas),
    "p_status": np.random.choice(["A", "I"], n_notas),
})
notamedicaurg.to_parquet(data_dir / "notamedicaurg.parquet", index=False)

print("\n✓ Datos dummy generados en data/01_raw/")
print(f"  - hospac: {len(hospac)} pacientes")
print(f"  - hosagd: {len(hosagd)} citas")
print(f"  - hosmpi: {len(hosmpi)} registros")
print(f"  - triage: {len(triage)} eventos")
print(f"  - notamedicaurg: {len(notamedicaurg)} notas")
