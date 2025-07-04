from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from config.settings import MONGODB_URI

print(f"Tentando conectar ao MongoDB: {MONGODB_URI}")

client = MongoClient(MONGODB_URI)

try:
    client.admin.command("ping")
    print("✅ Conexão com MongoDB estabelecida com sucesso!")
except Exception as e:
    print(f"❌ Erro ao conectar ao MongoDB: {e}")
    raise

db = client.spy

user_data_collection = db.spy_users
achievements_collection = db.spy_achievements
reports_collection = db.spy_reports
alerts_collection = db.spy_alerts
silence_collection = db.spy_silence


def test_connection():
    try:
        admin_db = MongoClient(MONGODB_URI, server_api=ServerApi("1")).get_database(
            "admin"
        )
        admin_db.command("ping")
        print("✅ Conectado com sucesso ao MongoDB!")
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar com MongoDB: {e}")
        return False
