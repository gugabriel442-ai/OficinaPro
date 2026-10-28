
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CA_CERT = os.path.join(BASE_DIR, "certificados", "ca.pem")


def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "oficina_db"),
        ssl_ca=CA_CERT,
        ssl_verify_cert=True
    )
