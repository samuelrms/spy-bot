from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from config.database import user_data_collection
from models.user import UserData
from utils.formatters import format_time


class UserService:
    @staticmethod
    def save_user_data(user_data: UserData) -> bool:
        try:
            document = user_data.to_mongodb()
            user_data_collection.update_one(
                {"user_id": user_data.user_id}, {"$set": document}, upsert=True
            )
            return True
        except Exception as e:
            print(f"Erro ao salvar dados no MongoDB: {e}")
            return False

    @staticmethod
    def get_user_data(user_id: str) -> Optional[UserData]:
        try:
            document = user_data_collection.find_one({"user_id": user_id})
            return UserData.from_mongodb(document)
        except Exception as e:
            print(f"Erro ao buscar dados no MongoDB: {e}")
            return None

    @staticmethod
    def update_status_time(
        user_id: str, new_status: str, member_name: str = ""
    ) -> UserData:
        user_data = UserService.get_user_data(user_id)

        if not user_data:
            user_data = UserData(user_id, member_name)
            user_data.current_status = str(new_status)
            user_data.status_start = datetime.now()
            print(
                f"[DEBUG] Novo usuário criado: {member_name} ({user_id}) com status: {new_status}"
            )
        else:
            if member_name:
                user_data.name = member_name

            current_time = datetime.now()
            if user_data.current_status and user_data.status_start:
                current_status_str = str(user_data.current_status)
                if current_status_str in user_data.status_time:
                    elapsed = current_time - user_data.status_start
                    user_data.status_time[current_status_str] += elapsed
                    print(
                        f"[DEBUG] Adicionado {format_time(elapsed)} ao status {current_status_str} para {user_data.name}"
                    )

            user_data.current_status = str(new_status)
            user_data.status_start = current_time
            print(f"[DEBUG] Status atualizado para {new_status} para {user_data.name}")

        print(f"[DEBUG] status_time salvo: {user_data.status_time}")
        UserService.save_user_data(user_data)
        return user_data

    @staticmethod
    def update_voice_time(
        user_id: str,
        channel_name: str,
        is_joining: bool,
        member_name: str = "",
        sala_excluida: str = None,
    ) -> UserData:
        user_data = UserService.get_user_data(user_id)

        if not user_data:
            user_data = UserData(user_id, member_name)
        else:
            if member_name:
                user_data.name = member_name

        current_time = datetime.now()

        if not is_joining and user_data.current_voice and user_data.voice_start:
            elapsed = current_time - user_data.voice_start

            user_data.total_voice_time += elapsed

            if user_data.current_voice != sala_excluida:
                if user_data.current_voice in user_data.voice_time:
                    user_data.voice_time[user_data.current_voice] += elapsed
                else:
                    user_data.voice_time[user_data.current_voice] = elapsed

        if is_joining:
            user_data.current_voice = channel_name
            user_data.voice_start = current_time
        else:
            user_data.current_voice = None
            user_data.voice_start = None

        UserService.save_user_data(user_data)
        return user_data

    @staticmethod
    def update_user_counter(user_id: str, field: str, increment: int = 1) -> bool:
        try:
            user_data_collection.update_one(
                {"user_id": user_id}, {"$inc": {field: increment}}, upsert=True
            )
            return True
        except Exception as e:
            print(f"Erro ao atualizar contador: {e}")
            return False

    @staticmethod
    def get_user_counter(user_id: str, field: str) -> int:
        try:
            doc = user_data_collection.find_one({"user_id": user_id})
            return doc.get(field, 0) if doc else 0
        except Exception as e:
            print(f"Erro ao obter contador: {e}")
            return 0

    @staticmethod
    def get_top_users(
        limit: int = 10, category: str = "online"
    ) -> List[Dict[str, Any]]:
        try:
            if category == "online":
                pipeline = [
                    {
                        "$project": {
                            "user_id": 1,
                            "name": 1,
                            "total_online": "$status_time.online",
                        }
                    },
                    {"$sort": {"total_online": -1}},
                    {"$limit": limit},
                ]
            elif category == "voice":
                pipeline = [
                    {
                        "$project": {
                            "user_id": 1,
                            "name": 1,
                            "total_voice": "$total_voice_time",
                        }
                    },
                    {"$sort": {"total_voice": -1}},
                    {"$limit": limit},
                ]
            else:
                return []

            results = list(user_data_collection.aggregate(pipeline))
            return results
        except Exception as e:
            print(f"Erro ao buscar top usuários: {e}")
            return []

    @staticmethod
    def check_inactive_users(alert_inactive_days: int) -> List[Dict[str, Any]]:
        try:
            cutoff_date = datetime.now() - timedelta(days=alert_inactive_days)

            inactive_users = user_data_collection.find(
                {"updated_at": {"$lt": cutoff_date}}
            )

            inactive_list = []
            for user in inactive_users:
                last_activity = user.get("updated_at", datetime.now())
                days_inactive = (datetime.now() - last_activity).days
                inactive_list.append(
                    {
                        "user_id": user["user_id"],
                        "name": user["name"],
                        "days_inactive": days_inactive,
                    }
                )

            return inactive_list
        except Exception as e:
            print(f"Erro ao verificar usuários inativos: {e}")
            return []
