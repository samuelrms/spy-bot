from typing import Any, Dict


class Achievement:
    def __init__(
        self,
        achievement_id: str,
        title: str,
        description: str,
        category: str = "Outros",
    ):
        self.achievement_id = achievement_id
        self.title = title
        self.description = description
        self.category = category
        self.user_id = None
        self.granted_at = None

    @classmethod
    def from_mongodb(cls, document: Dict[str, Any]) -> "Achievement":
        if not document:
            return None

        achievement = cls(
            document["achievement_id"],
            document["title"],
            document["description"],
            document.get("category", "Outros"),
        )
        achievement.user_id = document.get("user_id")
        achievement.granted_at = document.get("granted_at")

        return achievement

    def to_mongodb(self) -> Dict[str, Any]:
        return {
            "achievement_id": self.achievement_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "user_id": self.user_id,
            "granted_at": self.granted_at,
        }

    def is_granted(self) -> bool:
        return self.user_id is not None and self.granted_at is not None
