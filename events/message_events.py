import re

from config.settings import (
    HELP_KEYWORDS,
    PEACE_KEYWORDS,
    POLL_KEYWORDS,
    WELCOME_KEYWORDS,
)
from services.achievement_service import AchievementService
from services.sleep_service import SleepService
from services.user_service import UserService


class MessageEvents:
    @staticmethod
    async def handle_message(message, client):
        print(
            f"[on_message] Mensagem recebida de {message.author} ({message.author.id}): {message.content}"
        )

        if message.author.bot:
            return

        user_id = str(message.author.id)
        content = message.content.lower().strip()

        MessageEvents.check_message_achievements(message, user_id, client)

        if content.startswith("!stats"):
            from commands.stats_command import StatsCommand

            await StatsCommand.handle(message)
        elif content.startswith("!top"):
            from commands.top_command import TopCommand

            await TopCommand.handle(message)
        elif content == "!achievements-categories":
            from commands.achievements_command import AchievementsCommand

            await AchievementsCommand.handle_categories(message)
        elif content.startswith("!achievements"):
            from commands.achievements_command import AchievementsCommand

            await AchievementsCommand.handle(message)
        elif content.startswith("!compare"):
            from commands.stats_command import StatsCommand

            await StatsCommand.handle_compare(message)
        elif content.startswith("!serverstats"):
            from commands.stats_command import StatsCommand

            await StatsCommand.handle_serverstats(message)
        elif content.startswith("!help"):
            from commands.help_command import HelpCommand

            await HelpCommand.handle(message)
        elif content.startswith("!debug"):
            from commands.admin_commands import AdminCommands

            await AdminCommands.handle_debug(message)
        elif content.startswith("!clear"):
            from commands.admin_commands import AdminCommands

            await AdminCommands.handle_clear(message)
        elif content == "!silence":
            from commands.help_command import HelpCommand

            await HelpCommand.handle_silence(message)
        elif content.startswith("!sleep"):
            from commands.sleep_command import SleepCommand

            await SleepCommand.handle_sleep(message)
        elif content.startswith("!wake"):
            from commands.sleep_command import SleepCommand

            await SleepCommand.handle_wake(message)
        elif content.startswith("!status-sleep"):
            from commands.sleep_command import SleepCommand

            await SleepCommand.handle_status(message)

    @staticmethod
    def check_message_achievements(message, user_id: str, client):
        content = message.content.lower().strip()

        in_voice = False
        try:
            guild = message.guild
            if guild:
                member = guild.get_member(message.author.id)
                if member and member.voice and member.voice.channel:
                    in_voice = True
        except Exception:  # nosec
            pass
        if in_voice:
            jumpy_count = UserService.get_user_counter(user_id, "jumpy_count") + 1
            UserService.update_user_counter(user_id, "jumpy_count", 1)
            if jumpy_count >= 50 and not AchievementService.has_achievement(
                user_id, "jumpy"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "jumpy",
                    "🚀 Saltitante",
                    "Alternou entre voz e texto 50 vezes",
                    client,
                )

        url_pattern = re.compile(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        )
        if url_pattern.search(message.content):
            link_count = UserService.get_user_counter(user_id, "links_sent") + 1
            UserService.update_user_counter(user_id, "links_sent", 1)
            if link_count >= 10 and not AchievementService.has_achievement(
                user_id, "link_sharer"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "link_sharer",
                    "🔗 Compartilhador",
                    "Enviou 10 links",
                    client,
                )

        if message.attachments:
            for attachment in message.attachments:
                if (
                    attachment.filename.lower().endswith(".gif")
                    or "gif" in attachment.content_type
                ):
                    gif_count = UserService.get_user_counter(user_id, "gifs_sent") + 1
                    UserService.update_user_counter(user_id, "gifs_sent", 1)
                    if gif_count >= 25 and not AchievementService.has_achievement(
                        user_id, "gif_master"
                    ):
                        AchievementService.grant_achievement(
                            user_id,
                            "gif_master",
                            "🎞️ Mestre dos GIFs",
                            "Enviou 25 GIFs",
                            client,
                        )
                    break

        if message.attachments:
            attachment_count = UserService.get_user_counter(
                user_id, "attachments_sent"
            ) + len(message.attachments)
            UserService.update_user_counter(
                user_id, "attachments_sent", len(message.attachments)
            )
            if attachment_count >= 50 and not AchievementService.has_achievement(
                user_id, "attachment_king"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "attachment_king",
                    "📎 Anexo Supremo",
                    "Enviou 50 anexos",
                    client,
                )

        if message.content.strip().endswith("?"):
            question_count = UserService.get_user_counter(user_id, "questions_sent") + 1
            UserService.update_user_counter(user_id, "questions_sent", 1)
            if question_count >= 50 and not AchievementService.has_achievement(
                user_id, "questioner"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "questioner",
                    "❓ Pergunteiro",
                    "Enviou 50 perguntas",
                    client,
                )

        custom_emojis = re.findall(r"<a?:[a-zA-Z0-9_]+:\d+>", message.content)
        if custom_emojis:
            emoji_count = UserService.get_user_counter(
                user_id, "custom_emojis_used"
            ) + len(custom_emojis)
            UserService.update_user_counter(
                user_id, "custom_emojis_used", len(custom_emojis)
            )
            if emoji_count >= 20 and not AchievementService.has_achievement(
                user_id, "emoji_collector"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "emoji_collector",
                    "📦 Colecionador de Emojis",
                    "Usou 20 emojis personalizados",
                    client,
                )

        if message.stickers:
            sticker_count = UserService.get_user_counter(
                user_id, "stickers_sent"
            ) + len(message.stickers)
            UserService.update_user_counter(
                user_id, "stickers_sent", len(message.stickers)
            )
            if sticker_count >= 20 and not AchievementService.has_achievement(
                user_id, "sticker_star"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "sticker_star",
                    "🌟 Estrela de Figurinhas",
                    "Enviou 20 figurinhas",
                    client,
                )

        code_blocks = re.findall(r"```[\s\S]*?```", message.content)
        if code_blocks:
            code_count = UserService.get_user_counter(
                user_id, "code_blocks_sent"
            ) + len(code_blocks)
            UserService.update_user_counter(
                user_id, "code_blocks_sent", len(code_blocks)
            )
            if code_count >= 10 and not AchievementService.has_achievement(
                user_id, "code_sharer"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "code_sharer",
                    "💻 Codificador",
                    "Compartilhou 10 trechos de código",
                    client,
                )

        if (
            any(keyword in message.content.lower() for keyword in WELCOME_KEYWORDS)
            and message.mentions
        ):
            welcome_count = UserService.get_user_counter(user_id, "welcomes_given") + 1
            UserService.update_user_counter(user_id, "welcomes_given", 1)
            if welcome_count >= 10 and not AchievementService.has_achievement(
                user_id, "welcomer"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "welcomer",
                    "🤝 Bem-vindo!",
                    "Deu boas-vindas a 10 novos membros",
                    client,
                )

        if (
            any(keyword in message.content.lower() for keyword in HELP_KEYWORDS)
            and message.mentions
        ):
            support_count = UserService.get_user_counter(user_id, "supports_given") + 1
            UserService.update_user_counter(user_id, "supports_given", 1)
            if support_count >= 10 and not AchievementService.has_achievement(
                user_id, "supporter"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "supporter",
                    "🛡️ Apoiador",
                    "Respondendo 10 dúvidas alheias",
                    client,
                )

        if any(keyword in message.content.lower() for keyword in PEACE_KEYWORDS):
            peace_count = UserService.get_user_counter(user_id, "peace_efforts") + 1
            UserService.update_user_counter(user_id, "peace_efforts", 1)
            if peace_count >= 5 and not AchievementService.has_achievement(
                user_id, "rumor_stopper"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "rumor_stopper",
                    "🔇 Guardião da Paz",
                    "Moderou 5 discussões tensas",
                    client,
                )

        if any(keyword in message.content.lower() for keyword in POLL_KEYWORDS) and (
            "?" in message.content or ":" in message.content
        ):
            poll_count = UserService.get_user_counter(user_id, "polls_created") + 1
            UserService.update_user_counter(user_id, "polls_created", 1)
            if poll_count >= 5 and not AchievementService.has_achievement(
                user_id, "poll_creator"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "poll_creator",
                    "📊 Criador de Enquetes",
                    "Fez 5 enquetes",
                    client,
                )

        UserService.update_user_counter(user_id, "messages_sent", 1)
        if UserService.get_user_counter(user_id, "messages_sent") == 100:
            AchievementService.grant_achievement(
                user_id, "chatterbox", "💬 Tagarela", "100 mensagens enviadas", client
            )

        if content == "!help":
            UserService.update_user_counter(user_id, "help_used", 1)
            if UserService.get_user_counter(user_id, "help_used") == 10:
                AchievementService.grant_achievement(
                    user_id,
                    "help_friend",
                    "🤝 Ajuda Sempre",
                    "Usou !help 10 vezes",
                    client,
                )

        if SleepService.is_sleeping():
            return

        try:
            user_data = UserService.get_user_data(user_id)
            if user_data:
                message_count = user_data.get("message_count", 0)
                if message_count >= 100 and not AchievementService.has_achievement(
                    user_id, "chatterbox"
                ):
                    AchievementService.grant_achievement(
                        user_id,
                        "chatterbox",
                        "💬 Tagarela",
                        "Enviou 100 mensagens",
                        client,
                    )
                elif message_count >= 500 and not AchievementService.has_achievement(
                    user_id, "conversationalist"
                ):
                    AchievementService.grant_achievement(
                        user_id,
                        "conversationalist",
                        "🗣️ Conversador",
                        "Enviou 500 mensagens",
                        client,
                    )
                elif message_count >= 1000 and not AchievementService.has_achievement(
                    user_id, "social_butterfly"
                ):
                    AchievementService.grant_achievement(
                        user_id,
                        "social_butterfly",
                        "🦋 Borboleta Social",
                        "Enviou 1000 mensagens",
                        client,
                    )
        except Exception as e:
            print(f"❌ Erro ao verificar conquistas de mensagem: {e}")
