from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from config.database import achievements_collection, user_data_collection
from services.user_service import UserService
from utils.formatters import format_time


class ReportService:
    @staticmethod
    def generate_weekly_report() -> Optional[Dict[str, Any]]:
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)

            total_users = user_data_collection.count_documents({})
            active_users = user_data_collection.count_documents(
                {"updated_at": {"$gte": start_date}}
            )

            top_online = UserService.get_top_users(5, "online")
            top_voice = UserService.get_top_users(5, "voice")

            new_achievements = list(
                achievements_collection.find({"granted_at": {"$gte": start_date}})
            )

            report_data = {
                "period": {"start": start_date, "end": end_date},
                "stats": {
                    "total_users": total_users,
                    "active_users": active_users,
                    "activity_rate": (
                        round((active_users / total_users * 100), 2)
                        if total_users > 0
                        else 0
                    ),
                },
                "top_users": {"online": top_online, "voice": top_voice},
                "new_achievements": len(new_achievements),
                "generated_at": datetime.now(),
            }

            return report_data
        except Exception as e:
            print(f"Erro ao gerar relatório semanal: {e}")
            return None

    @staticmethod
    def check_inactive_users(alert_inactive_days: int) -> list:
        return UserService.check_inactive_users(alert_inactive_days)

    @staticmethod
    def format_weekly_report_embed(report_data: Dict[str, Any]) -> Dict[str, Any]:
        embed_data = {
            "title": "📊 Relatório Semanal de Atividade",
            "description": "Resumo da atividade dos membros na última semana",
            "color": 0x00FF00,
            "timestamp": datetime.now(),
            "fields": [],
        }

        embed_data["fields"].append(
            {
                "name": "📈 Estatísticas Gerais",
                "value": f"👥 **Total de Membros**: {report_data['stats']['total_users']}\n"
                f"🟢 **Membros Ativos**: {report_data['stats']['active_users']}\n"
                f"📊 **Taxa de Atividade**: {report_data['stats']['activity_rate']}%",
                "inline": False,
            }
        )

        if report_data["top_users"]["online"]:
            online_text = ""
            for i, user in enumerate(report_data["top_users"]["online"][:5], 1):
                time_str = format_time(timedelta(seconds=user.get("total_online", 0)))
                online_text += (
                    f"{i}. **{user.get('name', 'Desconhecido')}**: {time_str}\n"
                )
            embed_data["fields"].append(
                {"name": "🏆 Top 5 - Tempo Online", "value": online_text, "inline": True}
            )

        if report_data["top_users"]["voice"]:
            voice_text = ""
            for i, user in enumerate(report_data["top_users"]["voice"][:5], 1):
                time_str = format_time(timedelta(seconds=user.get("total_voice", 0)))
                voice_text += (
                    f"{i}. **{user.get('name', 'Desconhecido')}**: {time_str}\n"
                )
            embed_data["fields"].append(
                {"name": "🎤 Top 5 - Tempo em Voz", "value": voice_text, "inline": True}
            )

        embed_data["fields"].append(
            {
                "name": "🏆 Conquistas da Semana",
                "value": f"🎉 **{report_data['new_achievements']}** novas conquistas concedidas!",
                "inline": False,
            }
        )

        embed_data["footer"] = {"text": "Spy Bot • Relatório Semanal"}

        return embed_data

    @staticmethod
    def format_inactive_users_embed(inactive_users: list) -> Dict[str, Any]:
        embed_data = {
            "title": "⚠️ Alertas de Inatividade",
            "description": "Membros que não foram vistos recentemente",
            "color": 0xFF6B35,
            "timestamp": datetime.now(),
            "fields": [],
        }

        for user in inactive_users[:10]:
            embed_data["fields"].append(
                {
                    "name": f"👤 {user['name']}",
                    "value": f"📅 **{user['days_inactive']}** dias inativo",
                    "inline": True,
                }
            )

        embed_data["footer"] = {"text": "Spy Bot • Alertas de Inatividade"}

        return embed_data
