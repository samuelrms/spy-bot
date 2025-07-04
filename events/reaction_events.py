from config.settings import HEART_EMOJIS, POLL_KEYWORDS
from services.achievement_service import AchievementService
from services.user_service import UserService


class ReactionEvents:
    @staticmethod
    async def handle_reaction_add(reaction, user, client):
        if user.bot:
            return

        user_id = str(user.id)

        UserService.update_user_counter(user_id, "reactions_given", 1)
        if UserService.get_user_counter(user_id, "reactions_given") == 50:
            AchievementService.grant_achievement(
                user_id, "emoji_king", "😃 Rei do Emoji", "50 reações", client
            )

        if str(reaction.emoji) in HEART_EMOJIS:
            heart_count = UserService.get_user_counter(user_id, "heart_reactions") + 1
            UserService.update_user_counter(user_id, "heart_reactions", 1)
            if heart_count >= 30 and not AchievementService.has_achievement(
                user_id, "heartgiver"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "heartgiver",
                    "❤️ Amante do Like",
                    "Reagiu com coração 30 vezes",
                    client,
                )

        try:
            message = reaction.message
            if message and message.content:
                if any(keyword in message.content.lower() for keyword in POLL_KEYWORDS):
                    poll_vote_count = (
                        UserService.get_user_counter(user_id, "poll_votes") + 1
                    )
                    UserService.update_user_counter(user_id, "poll_votes", 1)
                    if (
                        poll_vote_count >= 20
                        and not AchievementService.has_achievement(
                            user_id, "poll_voter"
                        )
                    ):
                        AchievementService.grant_achievement(
                            user_id,
                            "poll_voter",
                            "✅ Eleitor de Enquetes",
                            "Votou em 20 enquetes",
                            client,
                        )
        except Exception:  # nosec
            pass
