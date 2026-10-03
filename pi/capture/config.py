
INTERFACE = "wlan1"
ANALYSIS_SECONDS = 10
SLEEP_SECONDS = 0
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "raw_occupancy.db"
CHANNELS = [1,6,11]