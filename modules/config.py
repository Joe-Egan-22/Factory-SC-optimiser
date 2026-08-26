from pathlib import Path
import os

BASE_DIRECTORY = Path(__file__).resolve().parents[1]

def get_settings():
    return {
        "database_dir": Path(os.getenv("FACTORY_DB_DIR", BASE_DIRECTORY / "Databases")),
        "max_labour_time": float(os.getenv("FACTORY_MAXTIME_LABOUR", 48)),
        "max_machine_time": float(os.getenv("FACTORY_MAXTIME_MACHINE", 60))
    }