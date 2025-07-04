import asyncio
from datetime import datetime, timedelta

import discord

from config.database import test_connection
from config.settings import ALERT_INACTIVE_DAYS, DISCORD_BOT_TOKEN, DISCORD_INTENTS
from events.message_events import MessageEvents
from events.presence_events import PresenceEvents
from events.reaction_events import ReactionEvents
from events.voice_events import VoiceEvents
from services.achievement_service import AchievementService
from services.report_service import ReportService
from services.sleep_service import SleepService

print("🚀 Iniciando bot...")

intents = discord.Intents.default()
for intent_name, enabled in DISCORD_INTENTS.items():
    setattr(intents, intent_name, enabled)

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """Evento executado quando o bot está pronto"""
    print(f"Bot logado como {client.user} (ID: {client.user.id})")
    print("--------------------------------------------------")
    print("Bot de monitoramento de status e salas de voz está online!")
    print("--------------------------------------------------")
    print("✅ Evento on_ready executado!")

    # Testa conexão com MongoDB
    if test_connection():
        print("✅ Conectado com sucesso ao MongoDB!")
    else:
        print("❌ Erro ao conectar com MongoDB!")

    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="tempo dos membros"
        )
    )

    client.loop.create_task(schedule_reports())
    client.loop.create_task(schedule_alerts())

    AchievementService.register_default_achievements()


@client.event
async def on_presence_update(before, after):
    await PresenceEvents.handle_presence_update(before, after, client)


@client.event
async def on_voice_state_update(member, before, after):
    await VoiceEvents.handle_voice_state_update(member, before, after, client)


@client.event
async def on_message(message):
    await MessageEvents.handle_message(message, client)


@client.event
async def on_reaction_add(reaction, user):
    await ReactionEvents.handle_reaction_add(reaction, user, client)


@client.event
async def on_member_join(member):
    if member.bot:
        return
    print(f"🎉 Novo membro: {member.display_name} ({member.id}) entrou no servidor!")


@client.event
async def on_invite_create(invite):
    print(
        f"📨 Convite criado por {invite.inviter.display_name if invite.inviter else 'Desconhecido'}"
    )


@client.event
async def on_invite_delete(invite):
    print("🗑️ Convite deletado")


@client.event
async def on_member_remove(member):
    if member.bot:
        return
    print(f"👋 Membro saiu: {member.display_name} ({member.id})")


async def schedule_reports():
    while True:
        try:
            now = datetime.now()

            days_ahead = 6 - now.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            next_sunday = now + timedelta(days=days_ahead)
            next_report_time = next_sunday.replace(
                hour=20, minute=0, second=0, microsecond=0
            )

            wait_seconds = (next_report_time - now).total_seconds()
            if wait_seconds > 0:
                print(f"📊 Próximo relatório semanal: {next_report_time}")
                await asyncio.sleep(wait_seconds)

            await send_weekly_report()

        except Exception as e:
            print(f"Erro no agendamento de relatórios: {e}")
            await asyncio.sleep(3600)


async def schedule_alerts():
    while True:
        try:
            await asyncio.sleep(86400)
            await check_and_send_alerts()
        except Exception as e:
            print(f"Erro no agendamento de alertas: {e}")
            await asyncio.sleep(3600)


async def send_weekly_report():
    from config.settings import CANAL_RELATORIOS_ID

    if not CANAL_RELATORIOS_ID:
        print("❌ Canal de relatórios não configurado")
        return

    if SleepService.is_sleeping():
        return

    try:
        canal = client.get_channel(CANAL_RELATORIOS_ID)
        if not canal:
            print(f"❌ Canal de relatórios {CANAL_RELATORIOS_ID} não encontrado")
            return

        report_data = ReportService.generate_weekly_report()
        if not report_data:
            print("❌ Erro ao gerar relatório semanal")
            return

        embed_data = ReportService.format_weekly_report_embed(report_data)

        embed = discord.Embed(
            title=embed_data["title"],
            description=embed_data["description"],
            color=embed_data["color"],
            timestamp=embed_data["timestamp"],
        )

        for field in embed_data["fields"]:
            embed.add_field(
                name=field["name"],
                value=field["value"],
                inline=field.get("inline", False),
            )

        embed.set_footer(text=embed_data["footer"]["text"])
        await canal.send(embed=embed)
        print("✅ Relatório semanal enviado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao enviar relatório semanal: {e}")


async def check_and_send_alerts():
    from config.settings import CANAL_ALERTAS_ID

    if not CANAL_ALERTAS_ID:
        return

    if SleepService.is_sleeping():
        return

    try:
        canal = client.get_channel(CANAL_ALERTAS_ID)
        if not canal:
            return

        inactive_users = ReportService.check_inactive_users(ALERT_INACTIVE_DAYS)
        if not inactive_users:
            return

        embed_data = ReportService.format_inactive_users_embed(inactive_users)

        embed = discord.Embed(
            title=embed_data["title"],
            description=embed_data["description"],
            color=embed_data["color"],
            timestamp=embed_data["timestamp"],
        )

        for field in embed_data["fields"]:
            embed.add_field(
                name=field["name"],
                value=field["value"],
                inline=field.get("inline", False),
            )

        embed.set_footer(text=embed_data["footer"]["text"])
        await canal.send(embed=embed)
        print(f"⚠️ Alerta de inatividade enviado para {len(inactive_users)} usuários")

    except Exception as e:
        print(f"❌ Erro ao enviar alertas: {e}")


if __name__ == "__main__":
    client.run(DISCORD_BOT_TOKEN)
