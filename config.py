from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")

MANAGER_ID=int(getenv("MANAGER_ID", 0))