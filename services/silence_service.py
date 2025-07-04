from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from config.database import silence_collection


class SilenceService:
    @staticmethod
    def set_user_silence(
        user_id: str,
        duration_hours: int = None,
        duration_days: int = None,
        permanent: bool = False,
    ) -> bool:
        try:
            if permanent:
                silence_until = None
            else:
                silence_until = datetime.now()
                if duration_hours:
                    silence_until += timedelta(hours=duration_hours)
                if duration_days:
                    silence_until += timedelta(days=duration_days)

            document = {
                "user_id": user_id,
                "silence_until": silence_until,
                "permanent": permanent,
                "set_at": datetime.now(),
            }

            silence_collection.update_one(
                {"user_id": user_id}, {"$set": document}, upsert=True
            )
            return True
        except Exception as e:
            print(f"Erro ao definir silenciamento: {e}")
            return False

    @staticmethod
    def remove_user_silence(user_id: str) -> bool:
        try:
            silence_collection.delete_one({"user_id": user_id})
            return True
        except Exception as e:
            print(f"Erro ao remover silenciamento: {e}")
            return False

    @staticmethod
    def is_user_silenced(user_id: str) -> bool:
        try:
            silence_data = silence_collection.find_one({"user_id": user_id})
            if not silence_data:
                return False

            if silence_data.get("permanent", False):
                return True

            silence_until = silence_data.get("silence_until")
            if not silence_until:
                return False

            return datetime.now() < silence_until
        except Exception as e:
            print(f"Erro ao verificar silenciamento: {e}")
            return False

    @staticmethod
    def get_user_silence_info(user_id: str) -> Optional[Dict[str, Any]]:
        try:
            silence_data = silence_collection.find_one({"user_id": user_id})
            if not silence_data:
                return None

            if silence_data.get("permanent", False):
                return {
                    "permanent": True,
                    "set_at": silence_data.get("set_at"),
                    "remaining": None,
                }

            silence_until = silence_data.get("silence_until")
            if not silence_until:
                return None

            remaining = silence_until - datetime.now()
            if remaining.total_seconds() <= 0:
                SilenceService.remove_user_silence(user_id)
                return None

            return {
                "permanent": False,
                "silence_until": silence_until,
                "set_at": silence_data.get("set_at"),
                "remaining": remaining,
            }
        except Exception as e:
            print(f"Erro ao obter informações de silenciamento: {e}")
            return None
