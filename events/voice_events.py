from datetime import datetime, timezone

from config.settings import SALA_EXCLUIDA
from services.achievement_service import AchievementService
from services.user_service import UserService


class VoiceEvents:
    @staticmethod
    async def handle_voice_state_update(member, before, after, client):
        print(
            f"[on_voice_state_update] {member.name} ({member.id}) mudou de sala de voz: {before.channel} -> {after.channel}"
        )

        if member.bot:
            return

        user_id = str(member.id)
        user_data = UserService.get_user_data(user_id) or {}
        current_time = datetime.now(timezone.utc)

        if (
            before.channel is not None
            and after.channel is not None
            and before.channel != after.channel
        ):
            count = user_data.get("voice_switches", 0) + 1
            UserService.update_user_counter(user_id, "voice_switches", 1)
            if count >= 20 and not AchievementService.has_achievement(
                user_id, "voice_switcher"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "voice_switcher",
                    "🔄 Troca de Sala",
                    "Mudou de canal de voz 20 vezes",
                    client,
                )

        if (
            after.channel is not None
            and hasattr(after.channel, "type")
            and str(after.channel.type) == "stage_voice"
        ):
            stage_count = user_data.get("stage_visited", 0) + 1
            UserService.update_user_counter(user_id, "stage_visited", 1)
            if stage_count >= 5 and not AchievementService.has_achievement(
                user_id, "stage_visitor"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "stage_visitor",
                    "🎙️ Visitante do Palco",
                    "Entrou em canal Stage 5 vezes",
                    client,
                )

        if (
            hasattr(after, "self_stream")
            and after.self_stream
            and (not before.self_stream)
        ):
            stream_count = user_data.get("stream_count", 0) + 1
            UserService.update_user_counter(user_id, "stream_count", 1)
            if stream_count >= 5 and not AchievementService.has_achievement(
                user_id, "streamer"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "streamer",
                    "📡 Transmissor",
                    "Entrou em streaming 5 vezes",
                    client,
                )

        if after.channel is not None:
            try:
                members = [m for m in after.channel.members if not m.bot]
                if len(members) >= 3:
                    group_count = user_data.get("group_calls", 0) + 1
                    UserService.update_user_counter(user_id, "group_calls", 1)
                    if group_count >= 3 and not AchievementService.has_achievement(
                        user_id, "group_caller"
                    ):
                        AchievementService.grant_achievement(
                            user_id,
                            "group_caller",
                            "📞 Conferencista",
                            "Participou de 3 chamadas em grupo",
                            client,
                        )
            except Exception:  # nosec
                pass

        if after.channel is not None and (not after.self_mute):
            speaker_rooms = set(user_data.get("speaker_rooms", []))
            speaker_rooms.add(after.channel.id)
            UserService.update_user_counter(
                user_id, "speaker_rooms", len(speaker_rooms)
            )
            if len(speaker_rooms) >= 5 and not AchievementService.has_achievement(
                user_id, "speaker"
            ):
                AchievementService.grant_achievement(
                    user_id,
                    "speaker",
                    "🗣️ Orador",
                    "Usou o microfone em 5 canais diferentes",
                    client,
                )

        if after.channel is not None:
            try:
                is_live = False
                if (
                    hasattr(after.channel, "type")
                    and str(after.channel.type) == "stage_voice"
                ):
                    is_live = True
                elif hasattr(after.channel, "is_live") and after.channel.is_live:
                    is_live = True
                if is_live:
                    podcast_count = user_data.get("podcast_count", 0) + 1
                    UserService.update_user_counter(user_id, "podcast_count", 1)
                    if podcast_count >= 3 and not AchievementService.has_achievement(
                        user_id, "podcast_guest"
                    ):
                        AchievementService.grant_achievement(
                            user_id,
                            "podcast_guest",
                            "🎧 Convidado de Podcast",
                            "Esteve em áudio ao vivo 3 vezes",
                            client,
                        )
            except Exception:  # nosec
                pass

        if before.channel is not None and after.channel is None:
            if user_data.get("voice_start"):
                join_time = user_data["voice_start"]
                if isinstance(join_time, str):
                    join_time = datetime.fromisoformat(join_time)
                session_time = current_time - join_time
                if member.voice and member.voice.self_mute:
                    silent_time = (
                        user_data.get("silent_time", 0) + session_time.total_seconds()
                    )
                    UserService.update_user_counter(
                        user_id, "silent_time", int(session_time.total_seconds())
                    )
                    if silent_time >= 3600 and not AchievementService.has_achievement(
                        user_id, "silent_runner"
                    ):
                        AchievementService.grant_achievement(
                            user_id,
                            "silent_runner",
                            "🤫 Silencioso",
                            "Ficou 1h em voz sem falar",
                            client,
                        )

        if before.channel is None and after.channel is not None:
            UserService.update_user_counter(user_id, "last_voice_join", 1)

        channel_name = after.channel.name if after.channel else None
        is_joining = before.channel is None and after.channel is not None

        UserService.update_voice_time(
            user_id, channel_name, is_joining, member.display_name, SALA_EXCLUIDA
        )

        print(
            f"[on_voice_state_update] Dados de voz atualizados no MongoDB "
            f"para {member.name} ({member.id})"
        )
