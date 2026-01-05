import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdf_downloads"
DOCX_DIR = DATA_DIR / "docx_output"
METADATA_PATH = DATA_DIR / "pdf_metadata.json"

for directory in [DATA_DIR, PDF_DIR, DOCX_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

TESSERACT_CMD = r"F:\tesseract\tesseract.exe"
GOOGLE_API_KEY = "AIzaSyB57F2IhecMmcuwT0EJf7e2GLncbtDY4Gg"

# URL
MAIN_URL = "https://daotaodaihoc.humg.edu.vn/#/quychequydinh"
API_LOC_QUYDINH = "https://daotaodaihoc.humg.edu.vn/api/web/w-locdsquydinh"