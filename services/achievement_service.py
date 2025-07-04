from datetime import datetime, timedelta
from typing import List

import discord

from config.database import achievements_collection
from models.achievement import Achievement


class AchievementService:
    @staticmethod
    def has_achievement(user_id: str, achievement_id: str) -> bool:
        try:
            result = achievements_collection.find_one(
                {"user_id": user_id, "achievement_id": achievement_id}
            )
            return result is not None
        except Exception as e:
            print(f"Erro ao verificar conquista: {e}")
            return False

    @staticmethod
    def grant_achievement(
        user_id: str, achievement_id: str, title: str, description: str, client=None
    ) -> bool:
        try:
            base = achievements_collection.find_one(
                {"achievement_id": achievement_id, "user_id": None}
            )
            category = base.get("category") if base else None

            achievement_data = {
                "user_id": user_id,
                "achievement_id": achievement_id,
                "title": title,
                "description": description,
                "category": category,
                "granted_at": datetime.now(),
            }
            achievements_collection.insert_one(achievement_data)
            print(f"🏆 Conquista concedida: {title} para usuário {user_id}")

            if client:
                client.loop.create_task(
                    AchievementService.send_achievement_notification(
                        client, user_id, title, description
                    )
                )

            return True
        except Exception as e:
            print(f"Erro ao conceder conquista: {e}")
            return False

    @staticmethod
    async def send_achievement_notification(
        client, user_id: str, title: str, description: str
    ):
        from config.settings import CANAL_DE_NOTIFICACAO_ID
        from services.silence_service import SilenceService
        from services.sleep_service import SleepService

        if SleepService.is_sleeping():
            return
        try:
            if SilenceService.is_user_silenced(user_id):
                print(
                    f"Usuário {user_id} está silenciado, não enviando notificação de conquista"
                )
                return

            canal = client.get_channel(CANAL_DE_NOTIFICACAO_ID)
            if not canal:
                return

            embed = discord.Embed(
                title="🏆 Nova Conquista Desbloqueada!",
                description=f"**{title}**\n{description}",
                color=0xFFD700,
                timestamp=datetime.now(),
            )

            try:
                user = await client.fetch_user(int(user_id))
                embed.set_author(
                    name=user.display_name, icon_url=user.display_avatar.url
                )
            except Exception:  # nosec
                embed.set_author(name="Membro do Servidor")

            embed.set_footer(text="Spy Bot • Sistema de Conquistas")
            await canal.send(embed=embed)

        except Exception as e:
            print(f"Erro ao enviar notificação de conquista: {e}")

    @staticmethod
    def get_user_achievements(user_id: str) -> List[Achievement]:
        try:
            documents = list(achievements_collection.find({"user_id": user_id}))
            return [Achievement.from_mongodb(doc) for doc in documents]
        except Exception as e:
            print(f"Erro ao buscar conquistas: {e}")
            return []

    @staticmethod
    def check_achievements(user_id: str, user_data, client=None):
        achievements = []

        total_online_time = user_data.status_time.get("online", timedelta())
        if total_online_time >= timedelta(
            hours=1
        ) and not AchievementService.has_achievement(user_id, "first_hour"):
            achievements.append(
                ("first_hour", "⏰ Primeira Hora", "Ficou online por 1 hora")
            )
        if total_online_time >= timedelta(
            hours=10
        ) and not AchievementService.has_achievement(user_id, "dedicated"):
            achievements.append(
                ("dedicated", "🔥 Dedicado", "Ficou online por 10 horas")
            )
        if total_online_time >= timedelta(
            hours=50
        ) and not AchievementService.has_achievement(user_id, "veteran"):
            achievements.append(("veteran", "👑 Veterano", "Ficou online por 50 horas"))

        total_voice_time = user_data.total_voice_time
        if total_voice_time >= timedelta(
            hours=1
        ) and not AchievementService.has_achievement(user_id, "voice_explorer"):
            achievements.append(
                (
                    "voice_explorer",
                    "🎤 Explorador de Voz",
                    "Passou 1 hora em salas de voz",
                )
            )
        if total_voice_time >= timedelta(
            hours=10
        ) and not AchievementService.has_achievement(user_id, "voice_master"):
            achievements.append(
                ("voice_master", "🎵 Mestre da Voz", "Passou 10 horas em salas de voz")
            )

        rooms_visited = len(user_data.voice_time)
        if rooms_visited >= 3 and not AchievementService.has_achievement(
            user_id, "social_butterfly"
        ):
            achievements.append(
                ("social_butterfly", "🦋 Borboleta Social", "Visitou 3 salas diferentes")
            )
        if rooms_visited >= 10 and not AchievementService.has_achievement(
            user_id, "room_explorer"
        ):
            achievements.append(
                (
                    "room_explorer",
                    "🏠 Explorador de Salas",
                    "Visitou 10 salas diferentes",
                )
            )

        for achievement_id, title, description in achievements:
            AchievementService.grant_achievement(
                user_id, achievement_id, title, description, client
            )

    @staticmethod
    def register_default_achievements():
        default_achievements = [
            (
                "first_voice",
                "🎤 Primeira Vez",
                "Entrou em um canal de voz pela primeira vez",
                "🎤 Voz & Presença",
            ),
            (
                "marathon_voice",
                "🏁 Maratona de Voz",
                "4 horas seguidas em voz",
                "🎤 Voz & Presença",
            ),
            (
                "early_bird",
                "🌅 Madrugador",
                "Entrou em voz entre 5h e 7h",
                "🎤 Voz & Presença",
            ),
            (
                "night_owl",
                "🦉 Corujão",
                "Entrou em voz entre 2h e 5h",
                "🎤 Voz & Presença",
            ),
            (
                "meeting_fan",
                "👥 Fã de Reunião",
                "Entrou em 10 canais de voz diferentes",
                "🎤 Voz & Presença",
            ),
            (
                "explorer",
                "🗺️ Explorador",
                "Visitou todos os canais de voz",
                "🎤 Voz & Presença",
            ),
            (
                "mic_king",
                "🎙️ Rei do Microfone",
                "10h em voz sem estar mutado",
                "🎤 Voz & Presença",
            ),
            (
                "voice_switcher",
                "🔄 Troca de Sala",
                "Mudou de canal de voz 20 vezes",
                "🎤 Voz & Presença",
            ),
            (
                "silent_runner",
                "🤫 Silencioso",
                "Ficou 1h em voz sem falar",
                "🎤 Voz & Presença",
            ),
            (
                "streamer",
                "📡 Transmissor",
                "Entrou em streaming 5 vezes",
                "🎤 Voz & Presença",
            ),
            (
                "group_caller",
                "📞 Conferencista",
                "Participou de 3 chamadas em grupo",
                "🎤 Voz & Presença",
            ),
            (
                "speaker",
                "🗣️ Orador",
                "Usou o microfone em 5 canais diferentes",
                "🎤 Voz & Presença",
            ),
            (
                "jumpy",
                "🚀 Saltitante",
                "Alternou entre voz e texto 50 vezes",
                "🎤 Voz & Presença",
            ),
            (
                "stage_visitor",
                "🎙️ Visitante do Palco",
                "Entrou em canal Stage 5 vezes",
                "🎤 Voz & Presença",
            ),
            (
                "podcast_guest",
                "🎧 Convidado de Podcast",
                "Esteve em áudio ao vivo 3 vezes",
                "🎤 Voz & Presença",
            ),
            (
                "chatterbox",
                "💬 Tagarela",
                "100 mensagens enviadas",
                "💬 Mensagens & Reações",
            ),
            (
                "help_friend",
                "🤝 Ajuda Sempre",
                "Usou !help 10 vezes",
                "💬 Mensagens & Reações",
            ),
            ("emoji_king", "😃 Rei do Emoji", "50 reações", "💬 Mensagens & Reações"),
            (
                "link_sharer",
                "🔗 Compartilhador",
                "Enviou 10 links",
                "💬 Mensagens & Reações",
            ),
            (
                "gif_master",
                "🎞️ Mestre dos GIFs",
                "Enviou 25 GIFs",
                "💬 Mensagens & Reações",
            ),
            (
                "attachment_king",
                "📎 Anexo Supremo",
                "Enviou 50 anexos",
                "💬 Mensagens & Reações",
            ),
            (
                "questioner",
                "❓ Pergunteiro",
                "Enviou 50 perguntas",
                "💬 Mensagens & Reações",
            ),
            (
                "emoji_collector",
                "📦 Colecionador de Emojis",
                "Usou 20 emojis personalizados",
                "💬 Mensagens & Reações",
            ),
            (
                "heartgiver",
                "❤️ Amante do Like",
                "Reagiu com coração 30 vezes",
                "💬 Mensagens & Reações",
            ),
            (
                "sticker_star",
                "🌟 Estrela de Figurinhas",
                "Enviou 20 figurinhas",
                "💬 Mensagens & Reações",
            ),
            (
                "code_sharer",
                "💻 Codificador",
                "Compartilhou 10 trechos de código",
                "💬 Mensagens & Reações",
            ),
            (
                "role_collector",
                "🎭 Colecionador de Cargos",
                "3+ cargos diferentes",
                "🦋 Social & Comunidade",
            ),
            ("top1", "🥇 Primeiro Lugar", "#1 no ranking", "📈 Engajamento & Uso"),
            (
                "never_sleeps",
                "🌙 Nunca Dorme",
                "24h online sem ficar offline",
                "⏰ Atividade & Consistência",
            ),
            (
                "vanished",
                "🕵️‍♂️ Sumido",
                "7 dias sem atividade",
                "⏰ Atividade & Consistência",
            ),
            (
                "loyal",
                "🛡️ Fiel Escudeiro",
                "30 dias seguidos ativo",
                "⏰ Atividade & Consistência",
            ),
            (
                "welcomer",
                "🤝 Bem-vindo!",
                "Deu boas-vindas a 10 novos membros",
                "🦋 Social & Comunidade",
            ),
            (
                "invite_master",
                "📨 Mestre de Convites",
                "Convidou 5 usuários",
                "🦋 Social & Comunidade",
            ),
            (
                "supporter",
                "🛡️ Apoiador",
                "Respondendo 10 dúvidas alheias",
                "🦋 Social & Comunidade",
            ),
            (
                "mentor",
                "👨‍🏫 Mentor",
                "Ajudou 5 membros com !help",
                "🦋 Social & Comunidade",
            ),
            (
                "event_participant",
                "🎉 Participante de Evento",
                "Participou de 3 eventos do servidor",
                "🦋 Social & Comunidade",
            ),
            (
                "rumor_stopper",
                "🔇 Guardião da Paz",
                "Moderou 5 discussões tensas",
                "🦋 Social & Comunidade",
            ),
            (
                "poll_creator",
                "📊 Criador de Enquetes",
                "Fez 5 enquetes",
                "🦋 Social & Comunidade",
            ),
            (
                "poll_voter",
                "✅ Eleitor de Enquetes",
                "Votou em 20 enquetes",
                "🦋 Social & Comunidade",
            ),
        ]

        for achievement_id, title, description, category in default_achievements:
            if not achievements_collection.find_one(
                {"achievement_id": achievement_id, "user_id": {"$exists": False}}
            ):
                achievements_collection.insert_one(
                    {
                        "achievement_id": achievement_id,
                        "title": title,
                        "description": description,
                        "category": category,
                        "user_id": None,
                        "granted_at": None,
                    }
                )
