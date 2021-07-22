import dotenv,os
from pathlib import Path
dotenv.load_dotenv()
GCP_MYSQL_HOST = os.getenv("gcp_host")
GCP_MYSQL_USER = os.getenv("gcp_user")
GCP_MYSQL_PASSWORD = os.getenv("gcp_password")
GMAIL_PASSWORD = os.getenv("gmail_password")
BASE_DIR = Path(__file__).resolve().parent