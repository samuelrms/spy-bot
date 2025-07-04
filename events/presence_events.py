from datetime import datetime, timezone

import discord

from config.settings import CANAL_DE_NOTIFICACAO_ID
from services.achievement_service import AchievementService
from services.sleep_service import SleepService
from services.user_service import UserService


class PresenceEvents:
    @staticmethod
    async def handle_presence_update(before, after, client):
        print(
            f"[DEBUG] Evento on_presence_update: {before.status} -> {after.status} para {after.name} ({after.id})"
        )

        if after.bot:
            return

        if before.status != after.status:
            print(
                f"[DEBUG] Mudança de status detectada: {before.status} -> {after.status} para {after.name}"
            )
            UserService.update_status_time(
                str(after.id), after.status, after.display_name
            )
            print(
                f"[DEBUG] update_status_time chamado para {after.name} ({after.id}) com status {after.status}"
            )

            await PresenceEvents.send_status_notification(before, after, client)

        user_id = str(after.id)
        now = datetime.now(timezone.utc)
        user_data = UserService.get_user_data(user_id) or {}

        last_activity = user_data.get("last_activity")
        if last_activity:
            if isinstance(last_activity, str):
                last_activity = datetime.fromisoformat(last_activity)
            if (now - last_activity).days >= 7:
                AchievementService.grant_achievement(
                    user_id, "vanished", "🕵️‍♂️ Sumido", "7 dias sem atividade", client
                )
        UserService.update_user_counter(user_id, "last_activity", 1)

        active_days = set(user_data.get("active_days", []))
        active_days.add(now.strftime("%Y-%m-%d"))
        UserService.update_user_counter(user_id, "active_days", len(active_days))
        if len(active_days) >= 30:
            days_sorted = sorted(active_days)
            from datetime import datetime as dt

            streak = 1
            for i in range(1, len(days_sorted)):
                d1 = dt.strptime(days_sorted[i - 1], "%Y-%m-%d")
                d2 = dt.strptime(days_sorted[i], "%Y-%m-%d")
                if (d2 - d1).days == 1:
                    streak += 1
                    if streak >= 30:
                        AchievementService.grant_achievement(
                            user_id,
                            "loyal",
                            "🛡️ Fiel Escudeiro",
                            "30 dias seguidos ativo",
                            client,
                        )
                        break
                else:
                    streak = 1

        member_obj = after
        if hasattr(member_obj, "roles"):
            if len([r for r in member_obj.roles if not r.is_default()]) >= 3:
                AchievementService.grant_achievement(
                    user_id,
                    "role_collector",
                    "🎭 Colecionador de Cargos",
                    "3+ cargos diferentes",
                    client,
                )

        if hasattr(after, "status") and after.status == discord.Status.online:
            online_since = user_data.get("online_since")
            if not online_since:
                UserService.update_user_counter(user_id, "online_since", 1)
            else:
                if isinstance(online_since, str):
                    online_since = datetime.fromisoformat(online_since)
                if (now - online_since).total_seconds() >= 24 * 3600:
                    AchievementService.grant_achievement(
                        user_id,
                        "never_sleeps",
                        "🌙 Nunca Dorme",
                        "24h online sem ficar offline",
                        client,
                    )
        else:
            UserService.update_user_counter(user_id, "online_since", 0)

        print(
            f"[on_presence_update] Dados de presença atualizados no MongoDB para {member_obj.name} ({member_obj.id})"
        )

    @staticmethod
    async def send_status_notification(before, after, client):
        if SleepService.is_sleeping():
            return
        canal_de_notificacao = client.get_channel(CANAL_DE_NOTIFICACAO_ID)

        if not canal_de_notificacao:
            print(
                f"ERRO: Canal de notificação com ID {CANAL_DE_NOTIFICACAO_ID} não encontrado ou inacessível."
            )
            print(
                "Verifique se o ID está correto e se o bot tem permissão para ver e enviar mensagens no canal."
            )
            return

        status_map = {
            discord.Status.online: "Online",
            discord.Status.offline: "Offline",
            discord.Status.idle: "Ausente",
            discord.Status.dnd: "Não Incomodar",
        }

        status_anterior_nome = status_map.get(before.status, "Desconhecido")
        status_atual_nome = status_map.get(after.status, "Desconhecido")

        is_entering_discord = (
            before.status == discord.Status.offline
            and after.status != discord.Status.offline
        )
        is_leaving_discord = (
            before.status != discord.Status.offline
            and after.status == discord.Status.offline
        )

        is_mobile = (
            hasattr(after, "desktop_status")
            and after.desktop_status == discord.Status.offline
            and after.mobile_status != discord.Status.offline
        )

        if before.status == discord.Status.offline and not is_entering_discord:
            return

        mensagem = ""
        title = "🔄 Mudança de Status"
        color = 0x808080

        if is_entering_discord:
            if is_mobile:
                title = "📱 Entrada no Discord"
                mensagem = f"**{after.display_name}** entrou no Discord via **Mobile**!"
                color = 0x00FF00
            else:
                title = "💻 Entrada no Discord"
                mensagem = (
                    f"**{after.display_name}** entrou no Discord via **Desktop**!"
                )
                color = 0x00FF00
        elif is_leaving_discord:
            if is_mobile:
                title = "📱 Saída do Discord"
                mensagem = f"**{after.display_name}** saiu do Discord via **Mobile**."
                color = 0xFF6B35
            else:
                title = "💻 Saída do Discord"
                mensagem = f"**{after.display_name}** saiu do Discord via **Desktop**."
                color = 0xFF6B35
        elif after.status == discord.Status.online:
            mensagem = f"**{after.display_name}** está **{status_atual_nome}**!"
            color = 0x00FF00
        elif after.status == discord.Status.idle:
            mensagem = (
                f"**{after.display_name}** está **{status_atual_nome}** (Ausente)."
            )
            color = 0xFFFF00
        elif after.status == discord.Status.dnd:
            mensagem = f"**{after.display_name}** está **{status_atual_nome}** (Não Incomodar)."
            color = 0xFF0000
        else:
            mensagem = f"**{after.display_name}** mudou de status: de {status_anterior_nome} para {status_atual_nome}."

        if mensagem:
            embed = discord.Embed(
                title=title,
                description=mensagem,
                color=color,
                timestamp=datetime.now(),
            )
            embed.set_author(name=after.display_name, icon_url=after.display_avatar.url)

            if is_entering_discord or is_leaving_discord:
                platform_info = "📱 Mobile" if is_mobile else "💻 Desktop"
                embed.add_field(name="🖥️ Plataforma", value=platform_info, inline=True)

            embed.set_footer(text="Spy Bot • Monitoramento de Status")
            await canal_de_notificacao.send(embed=embed)
