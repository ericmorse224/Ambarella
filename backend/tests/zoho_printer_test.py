from dotenv import load_dotenv
import os

load_dotenv(os.path.expanduser("~/.app_secrets/.env"))
print(os.getenv("ZOHO_CLIENT_ID"))

