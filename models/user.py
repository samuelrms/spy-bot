from datetime import datetime, timedelta
from typing import Any, Dict


class UserData:
    def __init__(self, user_id: str, name: str = ""):
        self.user_id = user_id
        self.name = name
        self.status_time = {
            "online": timedelta(),
            "offline": timedelta(),
            "idle": timedelta(),
            "dnd": timedelta(),
        }
        self.voice_time = {}
        self.total_voice_time = timedelta()
        self.current_status = None
        self.current_voice = None
        self.status_start = None
        self.voice_start = None
        self.updated_at = datetime.now()

    @classmethod
    def from_mongodb(cls, document: Dict[str, Any]) -> "UserData":
        if not document:
            return None

        user = cls(document["user_id"], document["name"])

        user.status_time = {
            k: timedelta(seconds=v) for k, v in document["status_time"].items()
        }
        user.voice_time = {
            k: timedelta(seconds=v) for k, v in document["voice_time"].items()
        }
        user.total_voice_time = timedelta(seconds=document.get("total_voice_time", 0))

        current_status = document.get("current_status", None)
        if isinstance(current_status, list):
            current_status = str(current_status[-1]) if current_status else "offline"
        else:
            current_status = str(current_status)

        user.current_status = current_status
        user.current_voice = document["current_voice"]
        user.status_start = document["status_start"]
        user.voice_start = document["voice_start"]

        return user

    def to_mongodb(self) -> Dict[str, Any]:
        status_time_seconds = {
            k: v.total_seconds() for k, v in self.status_time.items()
        }
        voice_time_seconds = {k: v.total_seconds() for k, v in self.voice_time.items()}
        total_voice_time_seconds = self.total_voice_time.total_seconds()

        return {
            "user_id": self.user_id,
            "name": self.name,
            "status_time": status_time_seconds,
            "voice_time": voice_time_seconds,
            "total_voice_time": total_voice_time_seconds,
            "current_status": self.current_status,
            "current_voice": self.current_voice,
            "status_start": self.status_start,
            "voice_start": self.voice_start,
            "updated_at": self.updated_at,
        }
