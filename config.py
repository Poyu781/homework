import dotenv,os
dotenv.load_dotenv()
gcp_mysql_host = os.getenv("gcp_host")
gcp_mysql_user = os.getenv("gcp_user")
gcp_mysql_password = os.getenv("gcp_password")