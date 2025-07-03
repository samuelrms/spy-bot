import os
from datetime import datetime, timedelta

import discord
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

print("🚀 Iniciando bot...")
load_dotenv()

CANAL_DE_NOTIFICACAO_ID = int(os.getenv("CANAL_DE_NOTIFICACAO_ID"))
SALA_EXCLUIDA = os.getenv("SALA_EXCLUIDA")

# Configurações para rankings e relatórios
CANAL_RELATORIOS_ID = int(os.getenv("CANAL_RELATORIOS_ID")) or None
CANAL_ALERTAS_ID = int(os.getenv("CANAL_ALERTAS_ID")) or None
REPORT_TIME = os.getenv("REPORT_TIME", "sunday 20:00")  # Domingo às 20h
ALERT_INACTIVE_DAYS = int(os.getenv("ALERT_INACTIVE_DAYS"))  # 7 dias

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
print(f"Tentando conectar ao MongoDB: {MONGODB_URI}")
client = MongoClient(MONGODB_URI)
try:
    # Testa a conexão
    client.admin.command("ping")
    print("✅ Conexão com MongoDB estabelecida com sucesso!")
except Exception as e:
    print(f"❌ Erro ao conectar ao MongoDB: {e}")
    raise

db = client.spy  # nome do banco
user_data_collection = db.spy_users  # nome da collection
achievements_collection = db.spy_achievements  # conquistas
reports_collection = db.spy_reports  # relatórios
alerts_collection = db.spy_alerts  # alertas

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.presences = True
intents.voice_states = True
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)


def save_user_data_to_mongodb(user_id, data):
    """Salva os dados do usuário no MongoDB"""
    try:
        # Converte timedelta para segundos para armazenamento
        status_time_seconds = {
            k: v.total_seconds() for k, v in data["status_time"].items()
        }
        voice_time_seconds = {
            k: v.total_seconds() for k, v in data["voice_time"].items()
        }
        total_voice_time_seconds = data.get(
            "total_voice_time", timedelta()
        ).total_seconds()

        document = {
            "user_id": user_id,
            "name": data["name"],
            "status_time": status_time_seconds,
            "voice_time": voice_time_seconds,
            "total_voice_time": total_voice_time_seconds,
            "current_status": data["current_status"],
            "current_voice": data["current_voice"],
            "status_start": data["status_start"],
            "voice_start": data["voice_start"],
            "updated_at": datetime.now(),
        }

        # Upsert: atualiza se existir, insere se não existir
        user_data_collection.update_one(
            {"user_id": user_id}, {"$set": document}, upsert=True
        )
    except Exception as e:
        print(f"Erro ao salvar dados no MongoDB: {e}")


def get_user_data_from_mongodb(user_id):
    """Busca os dados do usuário no MongoDB"""
    try:
        document = user_data_collection.find_one({"user_id": user_id})
        if document:
            # Converte segundos de volta para timedelta
            status_time = {
                k: timedelta(seconds=v) for k, v in document["status_time"].items()
            }
            voice_time = {
                k: timedelta(seconds=v) for k, v in document["voice_time"].items()
            }
            total_voice_time = timedelta(seconds=document.get("total_voice_time", 0))

            # Garante que current_status é string
            current_status = document.get("current_status", None)
            if isinstance(current_status, list):
                current_status = (
                    str(current_status[-1]) if current_status else "offline"
                )
            else:
                current_status = str(current_status)

            return {
                "name": document["name"],
                "status_time": status_time,
                "voice_time": voice_time,
                "total_voice_time": total_voice_time,
                "current_status": current_status,
                "current_voice": document["current_voice"],
                "status_start": document["status_start"],
                "voice_start": document["voice_start"],
            }
    except Exception as e:
        print(f"Erro ao buscar dados no MongoDB: {e}")
    return None


def format_time(td):
    """Formata um timedelta em formato legível"""
    if not td:
        return "0h 0m"

    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def update_status_time(user_id, new_status, member_name=""):
    """Atualiza o tempo de status do usuário"""
    user_data = get_user_data_from_mongodb(user_id)

    if not user_data:
        user_data = {
            "name": member_name,
            "status_time": {
                "online": timedelta(),
                "offline": timedelta(),
                "idle": timedelta(),
                "dnd": timedelta(),
            },
            "voice_time": {},
            "total_voice_time": timedelta(),
            "current_status": str(new_status),
            "current_voice": None,
            "status_start": datetime.now(),
            "voice_start": None,
        }
        print(
            f"[DEBUG] Novo usuário criado: {member_name} ({user_id}) "
            f"com status: {new_status}"
        )
    else:
        if member_name:
            user_data["name"] = member_name
        if "total_voice_time" not in user_data:
            user_data["total_voice_time"] = timedelta()

        current_time = datetime.now()
        if user_data["current_status"] and user_data["status_start"]:
            # Garante que current_status é string
            current_status_str = str(user_data["current_status"])
            if current_status_str in user_data["status_time"]:
                elapsed = current_time - user_data["status_start"]
                user_data["status_time"][current_status_str] += elapsed
                print(
                    f"[DEBUG] Adicionado {format_time(elapsed)} ao status "
                    f"{current_status_str} para {user_data['name']}"
                )
        user_data["current_status"] = str(new_status)
        user_data["status_start"] = current_time
        print(f"[DEBUG] Status atualizado para {new_status} para {user_data['name']}")

    print(f"[DEBUG] status_time salvo: {user_data['status_time']}")
    save_user_data_to_mongodb(user_id, user_data)
    return user_data


def update_voice_time(user_id, channel_name, is_joining, member_name=""):
    """Atualiza o tempo em salas de voz do usuário"""
    # Busca dados existentes do MongoDB
    user_data = get_user_data_from_mongodb(user_id)

    if not user_data:
        # Cria novo usuário se não existir
        user_data = {
            "name": member_name,
            "status_time": {
                "online": timedelta(),
                "offline": timedelta(),
                "idle": timedelta(),
                "dnd": timedelta(),
            },
            "voice_time": {},
            "total_voice_time": timedelta(),  # Tempo total em voz
            "current_status": None,
            "current_voice": None,
            "status_start": None,
            "voice_start": None,
        }
    else:
        # Atualiza nome se fornecido
        if member_name:
            user_data["name"] = member_name

        # Inicializa total_voice_time se não existir
        if "total_voice_time" not in user_data:
            user_data["total_voice_time"] = timedelta()

    current_time = datetime.now()

    # Processa saída de sala
    if not is_joining and user_data["current_voice"] and user_data["voice_start"]:
        elapsed = current_time - user_data["voice_start"]

        # Sempre adiciona ao tempo total em voz
        user_data["total_voice_time"] += elapsed

        # Só registra individualmente se não for a sala excluída
        if user_data["current_voice"] != SALA_EXCLUIDA:
            if user_data["current_voice"] in user_data["voice_time"]:
                user_data["voice_time"][user_data["current_voice"]] += elapsed
            else:
                user_data["voice_time"][user_data["current_voice"]] = elapsed

    # Atualiza sala atual
    if is_joining:
        user_data["current_voice"] = channel_name
        user_data["voice_start"] = current_time
    else:
        user_data["current_voice"] = None
        user_data["voice_start"] = None

    # Salva no MongoDB
    save_user_data_to_mongodb(user_id, user_data)

    # Verifica conquistas
    check_achievements(user_id, user_data)

    return user_data


def check_achievements(user_id, user_data):
    """Verifica e concede conquistas baseadas nos dados do usuário"""
    achievements = []

    # Conquistas de tempo online
    total_online_time = user_data["status_time"].get("online", timedelta())
    if total_online_time >= timedelta(hours=1) and not has_achievement(
        user_id, "first_hour"
    ):
        achievements.append(
            ("first_hour", "⏰ Primeira Hora", "Ficou online por 1 hora")
        )
    if total_online_time >= timedelta(hours=10) and not has_achievement(
        user_id, "dedicated"
    ):
        achievements.append(("dedicated", "🔥 Dedicado", "Ficou online por 10 horas"))
    if total_online_time >= timedelta(hours=50) and not has_achievement(
        user_id, "veteran"
    ):
        achievements.append(("veteran", "👑 Veterano", "Ficou online por 50 horas"))

    # Conquistas de voz
    total_voice_time = user_data.get("total_voice_time", timedelta())
    if total_voice_time >= timedelta(hours=1) and not has_achievement(
        user_id, "voice_explorer"
    ):
        achievements.append(
            ("voice_explorer", "🎤 Explorador de Voz", "Passou 1 hora em salas de voz")
        )
    if total_voice_time >= timedelta(hours=10) and not has_achievement(
        user_id, "voice_master"
    ):
        achievements.append(
            ("voice_master", "🎵 Mestre da Voz", "Passou 10 horas em salas de voz")
        )

    # Conquistas de salas visitadas
    rooms_visited = len(user_data["voice_time"])
    if rooms_visited >= 3 and not has_achievement(user_id, "social_butterfly"):
        achievements.append(
            ("social_butterfly", "🦋 Borboleta Social", "Visitou 3 salas diferentes")
        )
    if rooms_visited >= 10 and not has_achievement(user_id, "room_explorer"):
        achievements.append(
            ("room_explorer", "🏠 Explorador de Salas", "Visitou 10 salas diferentes")
        )

    # Concede as conquistas
    for achievement_id, title, description in achievements:
        grant_achievement(user_id, achievement_id, title, description)


def has_achievement(user_id, achievement_id):
    """Verifica se o usuário já tem uma conquista específica"""
    try:
        result = achievements_collection.find_one(
            {"user_id": user_id, "achievement_id": achievement_id}
        )
        return result is not None
    except Exception as e:
        print(f"Erro ao verificar conquista: {e}")
        return False


def grant_achievement(user_id, achievement_id, title, description):
    """Concede uma conquista ao usuário"""
    try:
        achievement_data = {
            "user_id": user_id,
            "achievement_id": achievement_id,
            "title": title,
            "description": description,
            "granted_at": datetime.now(),
        }
        achievements_collection.insert_one(achievement_data)
        print(f"🏆 Conquista concedida: {title} para usuário {user_id}")

        # Envia notificação de conquista
        client.loop.create_task(
            send_achievement_notification(user_id, title, description)
        )

        return True
    except Exception as e:
        print(f"Erro ao conceder conquista: {e}")
        return False


async def send_achievement_notification(user_id, title, description):
    """Envia notificação de conquista no canal de notificações"""
    try:
        canal = client.get_channel(CANAL_DE_NOTIFICACAO_ID)
        if not canal:
            return

        embed = discord.Embed(
            title="🏆 Nova Conquista Desbloqueada!",
            description=f"**{title}**\n{description}",
            color=0xFFD700,
            timestamp=datetime.now(),
        )

        # Tenta buscar o usuário para mostrar o avatar
        try:
            user = await client.fetch_user(int(user_id))
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
        except Exception:  # noqa: E722
            embed.set_author(name="Membro do Servidor")

        embed.set_footer(text="Spy Bot • Sistema de Conquistas")
        await canal.send(embed=embed)

    except Exception as e:
        print(f"Erro ao enviar notificação de conquista: {e}")


def get_user_achievements(user_id):
    """Retorna todas as conquistas de um usuário"""
    try:
        achievements = list(achievements_collection.find({"user_id": user_id}))
        return achievements
    except Exception as e:
        print(f"Erro ao buscar conquistas: {e}")
        return []


def get_top_users(limit=10, category="online"):
    """Retorna os top usuários em uma categoria específica"""
    try:
        if category == "online":
            # Ordena por tempo total online
            pipeline = [
                {
                    "$project": {
                        "user_id": 1,
                        "name": 1,
                        "total_online": "$status_time.online",
                    }
                },
                {"$sort": {"total_online": -1}},
                {"$limit": limit},
            ]
        elif category == "voice":
            # Ordena por tempo total em voz
            pipeline = [
                {
                    "$project": {
                        "user_id": 1,
                        "name": 1,
                        "total_voice": "$total_voice_time",
                    }
                },
                {"$sort": {"total_voice": -1}},
                {"$limit": limit},
            ]
        else:
            return []

        results = list(user_data_collection.aggregate(pipeline))
        return results
    except Exception as e:
        print(f"Erro ao buscar top usuários: {e}")
        return []


def check_inactive_users():
    """Verifica usuários inativos e envia alertas"""
    try:
        cutoff_date = datetime.now() - timedelta(days=ALERT_INACTIVE_DAYS)

        # Busca usuários que não atualizaram dados recentemente
        inactive_users = user_data_collection.find({"updated_at": {"$lt": cutoff_date}})

        inactive_list = []
        for user in inactive_users:
            last_activity = user.get("updated_at", datetime.now())
            days_inactive = (datetime.now() - last_activity).days
            inactive_list.append(
                {
                    "user_id": user["user_id"],
                    "name": user["name"],
                    "days_inactive": days_inactive,
                }
            )

        return inactive_list
    except Exception as e:
        print(f"Erro ao verificar usuários inativos: {e}")
        return []


def generate_weekly_report():
    """Gera relatório semanal de atividade"""
    try:
        # Período da semana
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        # Estatísticas gerais
        total_users = user_data_collection.count_documents({})
        active_users = user_data_collection.count_documents(
            {"updated_at": {"$gte": start_date}}
        )

        # Top usuários da semana
        top_online = get_top_users(5, "online")
        top_voice = get_top_users(5, "voice")

        # Conquistas concedidas na semana
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


@client.event
async def on_ready():
    print(f"Bot logado como {client.user} (ID: {client.user.id})")
    print("--------------------------------------------------")
    print("Bot de monitoramento de status e salas de voz está online!")
    print("--------------------------------------------------")
    print("✅ Evento on_ready executado!")

    # Testa conexão com MongoDB
    admin_db = MongoClient(MONGODB_URI, server_api=ServerApi("1")).get_database("admin")
    try:
        admin_db.command("ping")
        print("✅ Conectado com sucesso ao MongoDB!")
    except Exception as e:
        print(f"❌ Erro ao conectar com MongoDB: {e}")

    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="tempo dos membros"
        )
    )

    # Inicia tarefas agendadas
    client.loop.create_task(schedule_reports())
    client.loop.create_task(schedule_alerts())


async def schedule_reports():
    """Agenda relatórios semanais"""
    import asyncio
    from datetime import datetime, timedelta

    while True:
        try:
            now = datetime.now()

            # Calcula próximo domingo às 20h
            days_ahead = 6 - now.weekday()  # 6 = domingo
            if days_ahead <= 0:  # Se já passou do domingo
                days_ahead += 7
            next_sunday = now + timedelta(days=days_ahead)
            next_report_time = next_sunday.replace(
                hour=20, minute=0, second=0, microsecond=0
            )

            # Aguarda até o próximo relatório
            wait_seconds = (next_report_time - now).total_seconds()
            if wait_seconds > 0:
                print(f"📊 Próximo relatório semanal: {next_report_time}")
                await asyncio.sleep(wait_seconds)

            # Gera e envia relatório
            await send_weekly_report()

        except Exception as e:
            print(f"Erro no agendamento de relatórios: {e}")
            await asyncio.sleep(3600)  # Aguarda 1 hora em caso de erro


async def schedule_alerts():
    """Agenda verificações de usuários inativos"""
    import asyncio

    while True:
        try:
            await asyncio.sleep(86400)  # Verifica a cada 24 horas
            await check_and_send_alerts()
        except Exception as e:
            print(f"Erro no agendamento de alertas: {e}")
            await asyncio.sleep(3600)


async def send_weekly_report():
    """Envia relatório semanal"""
    if not CANAL_RELATORIOS_ID:
        print("❌ Canal de relatórios não configurado")
        return

    try:
        canal = client.get_channel(CANAL_RELATORIOS_ID)
        if not canal:
            print(f"❌ Canal de relatórios {CANAL_RELATORIOS_ID} não encontrado")
            return

        report_data = generate_weekly_report()
        if not report_data:
            print("❌ Erro ao gerar relatório semanal")
            return

        embed = discord.Embed(
            title="📊 Relatório Semanal de Atividade",
            description="Resumo da atividade dos membros na última semana",
            color=0x00FF00,
            timestamp=datetime.now(),
        )

        # Estatísticas gerais
        embed.add_field(
            name="📈 Estatísticas Gerais",
            value=f"👥 **Total de Membros**: {report_data['stats']['total_users']}\n"
            f"🟢 **Membros Ativos**: {report_data['stats']['active_users']}\n"
            f"📊 **Taxa de Atividade**: {report_data['stats']['activity_rate']}%",
            inline=False,
        )

        # Top usuários online
        if report_data["top_users"]["online"]:
            online_text = ""
            for i, user in enumerate(report_data["top_users"]["online"][:5], 1):
                time_str = format_time(timedelta(seconds=user.get("total_online", 0)))
                online_text += (
                    f"{i}. **{user.get('name', 'Desconhecido')}**: {time_str}\n"
                )
            embed.add_field(
                name="🏆 Top 5 - Tempo Online", value=online_text, inline=True
            )

        # Top usuários em voz
        if report_data["top_users"]["voice"]:
            voice_text = ""
            for i, user in enumerate(report_data["top_users"]["voice"][:5], 1):
                time_str = format_time(timedelta(seconds=user.get("total_voice", 0)))
                voice_text += (
                    f"{i}. **{user.get('name', 'Desconhecido')}**: {time_str}\n"
                )
            embed.add_field(
                name="🎤 Top 5 - Tempo em Voz", value=voice_text, inline=True
            )

        # Conquistas da semana
        embed.add_field(
            name="🏆 Conquistas da Semana",
            value=(
                f"🎉 **{report_data['new_achievements']}** "
                "novas conquistas concedidas!"
            ),
            inline=False,
        )

        embed.set_footer(text="Spy Bot • Relatório Semanal")
        await canal.send(embed=embed)
        print("✅ Relatório semanal enviado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao enviar relatório semanal: {e}")


async def check_and_send_alerts():
    """Verifica e envia alertas de usuários inativos"""
    if not CANAL_ALERTAS_ID:
        return

    try:
        canal = client.get_channel(CANAL_ALERTAS_ID)
        if not canal:
            return

        inactive_users = check_inactive_users()
        if not inactive_users:
            return

        embed = discord.Embed(
            title="⚠️ Alertas de Inatividade",
            description="Membros que não foram vistos recentemente",
            color=0xFF6B35,
            timestamp=datetime.now(),
        )

        for user in inactive_users[:10]:  # Limita a 10 usuários
            embed.add_field(
                name=f"👤 {user['name']}",
                value=f"📅 **{user['days_inactive']}** dias inativo",
                inline=True,
            )

        embed.set_footer(text="Spy Bot • Alertas de Inatividade")
        await canal.send(embed=embed)
        print(f"⚠️ Alerta de inatividade enviado para {len(inactive_users)} usuários")

    except Exception as e:
        print(f"❌ Erro ao enviar alertas: {e}")


@client.event
async def on_presence_update(before, after):
    print(
        f"[DEBUG] Evento on_presence_update: {before.status} -> "
        f"{after.status} para {after.name} ({after.id})"
    )
    if after.bot:
        return

    if before.status != after.status:
        print(
            f"[DEBUG] Mudança de status detectada: {before.status} -> "
            f"{after.status} para {after.name}"
        )
        update_status_time(str(after.id), after.status, after.display_name)
        print(
            f"[DEBUG] update_status_time chamado para {after.name} "
            f"({after.id}) com status {after.status}"
        )

        canal_de_notificacao = client.get_channel(CANAL_DE_NOTIFICACAO_ID)

        if not canal_de_notificacao:
            print(
                f"ERRO: Canal de notificação com ID {CANAL_DE_NOTIFICACAO_ID} "
                "não encontrado ou inacessível."
            )
            print(
                "Verifique se o ID está correto e se o bot tem permissão "
                "para ver e enviar mensagens no canal."
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

        # Detecta se é uma entrada ou saída do Discord
        is_entering_discord = (
            before.status == discord.Status.offline
            and after.status != discord.Status.offline
        )
        is_leaving_discord = (
            before.status != discord.Status.offline
            and after.status == discord.Status.offline
        )

        # Detecta se está usando mobile
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
                f"**{after.display_name}** está **{status_atual_nome}** " "(Ausente)."
            )
            color = 0xFFFF00
        elif after.status == discord.Status.dnd:
            mensagem = (
                f"**{after.display_name}** está **{status_atual_nome}** "
                "(Não Incomodar)."
            )
            color = 0xFF0000
        else:
            mensagem = (
                f"**{after.display_name}** mudou de status: de "
                f"{status_anterior_nome} para {status_atual_nome}."
            )

        if mensagem:
            embed = discord.Embed(
                title=title,
                description=mensagem,
                color=color,
                timestamp=datetime.now(),
            )
            embed.set_author(name=after.display_name, icon_url=after.display_avatar.url)

            # Adiciona informações sobre a plataforma se relevante
            if is_entering_discord or is_leaving_discord:
                platform_info = "📱 Mobile" if is_mobile else "💻 Desktop"
                embed.add_field(name="🖥️ Plataforma", value=platform_info, inline=True)

            embed.set_footer(text="Spy Bot • Monitoramento de Status")
            await canal_de_notificacao.send(embed=embed)


@client.event
async def on_voice_state_update(member, before, after):
    print(
        f"[on_voice_state_update] {member.name} ({member.id}) mudou de sala de voz: "
        f"{before.channel} -> {after.channel}"
    )
    if member.bot:
        return

    user_id = str(member.id)

    if before.channel is None and after.channel is not None:
        channel_name = after.channel.name
        # Sempre atualiza o tempo (incluindo sala excluída)
        update_voice_time(user_id, channel_name, True, member.display_name)
        print(
            f"[on_voice_state_update] {member.name} entrou na sala "
            f"{after.channel.name}"
        )

        # Só envia notificação se não for a sala excluída
        if channel_name != SALA_EXCLUIDA:
            canal_de_notificacao = client.get_channel(CANAL_DE_NOTIFICACAO_ID)
            if canal_de_notificacao:
                embed = discord.Embed(
                    title="🎤 Entrada em Sala de Voz",
                    description=(
                        f"**{member.display_name}** entrou na sala "
                        f"**{channel_name}**"
                    ),
                    color=0x00FF00,
                    timestamp=datetime.now(),
                )
                embed.set_author(
                    name=member.display_name, icon_url=member.display_avatar.url
                )
                embed.add_field(name="📍 Sala", value=channel_name, inline=True)
                embed.set_footer(text="Spy Bot • Monitoramento de Voz")
                await canal_de_notificacao.send(embed=embed)

    elif before.channel is not None and after.channel is None:
        channel_name = before.channel.name
        # Sempre atualiza o tempo (incluindo sala excluída)
        user_data = update_voice_time(user_id, channel_name, False, member.display_name)
        print(
            f"[on_voice_state_update] {member.name} saiu da sala "
            f"{before.channel.name}"
        )

        # Só envia notificação se não for a sala excluída
        if channel_name != SALA_EXCLUIDA:
            if user_data and channel_name in user_data["voice_time"]:
                total_time = format_time(user_data["voice_time"][channel_name])

                canal_de_notificacao = client.get_channel(CANAL_DE_NOTIFICACAO_ID)
                if canal_de_notificacao:
                    embed = discord.Embed(
                        title="👋 Saída de Sala de Voz",
                        description=(
                            f"**{member.display_name}** saiu da sala "
                            f"**{channel_name}**"
                        ),
                        color=0xFF6B35,
                        timestamp=datetime.now(),
                    )
                    embed.set_author(
                        name=member.display_name, icon_url=member.display_avatar.url
                    )
                    embed.add_field(name="📍 Sala", value=channel_name, inline=True)
                    embed.add_field(
                        name="⏱️ Tempo Total",
                        value=total_time,
                        inline=True,
                    )
                    embed.set_footer(text="Spy Bot • Monitoramento de Voz")
                    await canal_de_notificacao.send(embed=embed)

    elif (
        before.channel is not None
        and after.channel is not None
        and before.channel != after.channel
    ):
        old_channel = before.channel.name
        new_channel = after.channel.name

        # Sempre atualiza o tempo (incluindo sala excluída)
        update_voice_time(user_id, old_channel, False, member.display_name)
        update_voice_time(user_id, new_channel, True, member.display_name)

        # Lógica de notificações para mudança de sala
        canal_de_notificacao = client.get_channel(CANAL_DE_NOTIFICACAO_ID)
        if canal_de_notificacao:
            # Caso 1: Mudança normal entre salas (nenhuma é a excluída)
            if old_channel != SALA_EXCLUIDA and new_channel != SALA_EXCLUIDA:
                embed = discord.Embed(
                    title="🔄 Mudança de Sala",
                    description=f"**{member.display_name}** mudou de sala",
                    color=0x0099FF,
                    timestamp=datetime.now(),
                )
                embed.set_author(
                    name=member.display_name, icon_url=member.display_avatar.url
                )
                embed.add_field(name="📍 Sala Anterior", value=old_channel, inline=True)
                embed.add_field(name="🎯 Nova Sala", value=new_channel, inline=True)
                embed.set_footer(text="Spy Bot • Monitoramento de Voz")
                await canal_de_notificacao.send(embed=embed)

            # Caso 2: Saiu de uma sala normal e foi para a sala excluída
            elif old_channel != SALA_EXCLUIDA and new_channel == SALA_EXCLUIDA:
                embed = discord.Embed(
                    title="👋 Saída de Sala de Voz",
                    description=(
                        f"**{member.display_name}** saiu da sala " f"**{old_channel}**"
                    ),
                    color=0xFF6B35,
                    timestamp=datetime.now(),
                )
                embed.set_author(
                    name=member.display_name, icon_url=member.display_avatar.url
                )
                embed.add_field(name="📍 Sala", value=old_channel, inline=True)
                embed.set_footer(text="Spy Bot • Monitoramento de Voz")
                await canal_de_notificacao.send(embed=embed)

            # Caso 3: Saiu da sala excluída e foi para uma sala normal
            elif old_channel == SALA_EXCLUIDA and new_channel != SALA_EXCLUIDA:
                embed = discord.Embed(
                    title="🎤 Entrada em Sala de Voz",
                    description=(
                        f"**{member.display_name}** entrou na sala "
                        f"**{new_channel}**"
                    ),
                    color=0x00FF00,
                    timestamp=datetime.now(),
                )
                embed.set_author(
                    name=member.display_name, icon_url=member.display_avatar.url
                )
                embed.add_field(name="📍 Sala", value=new_channel, inline=True)
                embed.set_footer(text="Spy Bot • Monitoramento de Voz")
                await canal_de_notificacao.send(embed=embed)

            # Caso 4: Mudança dentro da sala excluída
            # (não deve acontecer, mas por segurança)
            # elif old_channel == SALA_EXCLUIDA and new_channel == SALA_EXCLUIDA:
            #     # Não envia notificação
            #     pass

    print(
        f"[on_voice_state_update] Dados de voz atualizados no MongoDB "
        f"para {member.name} ({member.id})"
    )


@client.event
async def on_message(message):
    print(
        f"[on_message] Mensagem recebida de {message.author} "
        f"({message.author.id}): {message.content}"
    )
    if message.author.bot:
        return

    content = message.content.lower().strip()

    # Comando !stats (expandido)
    if content.startswith("!stats"):
        await handle_stats_command(message)

    # Comando !top
    elif content.startswith("!top"):
        await handle_top_command(message)

    # Comando !achievements
    elif content.startswith("!achievements"):
        await handle_achievements_command(message)

    # Comando !compare
    elif content.startswith("!compare"):
        await handle_compare_command(message)

    # Comando !serverstats
    elif content.startswith("!serverstats"):
        await handle_serverstats_command(message)

    # Comando !help
    elif content.startswith("!help"):
        await handle_help_command(message)

    # Comando !debug (apenas para desenvolvimento)
    elif content.startswith("!debug"):
        await handle_debug_command(message)


async def handle_stats_command(message):
    """Manipula o comando !stats"""
    user_id = str(message.author.id)
    user = get_user_data_from_mongodb(user_id)

    if user:
        # Calcular tempo atual no canal de voz se estiver em um
        current_voice_time = timedelta()
        if user["current_voice"] and user["voice_start"]:
            current_voice_time = datetime.now() - user["voice_start"]

        embed = discord.Embed(
            title=f"📊 Estatísticas de {user['name']}",
            color=0x00FF00,
            timestamp=datetime.now(),
        )
        embed.set_author(name=user["name"], icon_url=message.author.display_avatar.url)

        # Tempo por Status
        status_text = ""
        status_emojis = {"online": "🟢", "offline": "⚫", "idle": "🟡", "dnd": "🔴"}

        for status, time in user["status_time"].items():
            if status == user["current_status"] and user["status_start"]:
                current_time = datetime.now() - user["status_start"]
                total_time = time + current_time
                status_text += (
                    f"{status_emojis.get(status, '❓')} **{status.title()}**: "
                    f"{format_time(total_time)} *(atual)*\n"
                )
            else:
                total_time = time
                status_text += (
                    f"{status_emojis.get(status, '❓')} **{status.title()}**: "
                    f"{format_time(total_time)}\n"
                )

        embed.add_field(name="⏰ Tempo por Status", value=status_text, inline=False)

        # Tempo atual no canal de voz
        if user["current_voice"] and user["voice_start"]:
            embed.add_field(
                name="🎤 Canal Atual",
                value=(
                    f"**{user['current_voice']}**: "
                    f"{format_time(current_voice_time)} *(em andamento)*"
                ),
                inline=False,
            )

        # Tempo Total em Voz
        total_voice_time = user.get("total_voice_time", timedelta())
        if user["current_voice"] and user["voice_start"]:
            current_time = datetime.now() - user["voice_start"]
            total_voice_time += current_time

        embed.add_field(
            name="🎤 Tempo Total em Voz",
            value=f"**{format_time(total_voice_time)}**",
            inline=True,
        )

        # Tempo em Salas de Voz (exceto sala excluída)
        if user["voice_time"]:
            voice_text = ""
            for room, time in user["voice_time"].items():
                if room == user["current_voice"] and user["voice_start"]:
                    current_time = datetime.now() - user["voice_start"]
                    total_time = time + current_time
                    voice_text += (
                        f"🎤 **{room}**: {format_time(total_time)} " f"*(atual)*\n"
                    )
                else:
                    total_time = time
                    voice_text += f"🎤 **{room}**: {format_time(total_time)}\n"

            if (
                user["current_voice"]
                and user["current_voice"] not in user["voice_time"]
                and user["current_voice"] != SALA_EXCLUIDA
            ):
                current_time = datetime.now() - user["voice_start"]
                voice_text += (
                    f"🎤 **{user['current_voice']}**: "
                    f"{format_time(current_time)} *(atual)*\n"
                )

            embed.add_field(name="🎤 Salas de Voz", value=voice_text, inline=False)
        else:
            embed.add_field(
                name="🎤 Salas de Voz",
                value="*Nenhuma sala visitada ainda*",
                inline=False,
            )

        # Conquistas do usuário
        achievements = get_user_achievements(user_id)
        if achievements:
            achievements_text = ""
            for achievement in achievements[:5]:  # Mostra apenas as 5 primeiras
                achievements_text += (
                    f"🏆 **{achievement['title']}**: {achievement['description']}\n"
                )
            embed.add_field(name="🏆 Conquistas", value=achievements_text, inline=False)

        embed.set_footer(text="Spy Bot • Estatísticas")
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ Dados Não Encontrados",
            description=(
                "Nenhum dado de monitoramento foi encontrado para " "você ainda."
            ),
            color=0xFF0000,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.display_avatar.url,
        )
        embed.add_field(
            name="💡 Dica",
            value=(
                "Entre em uma sala de voz ou mude seu status para "
                "começar a coletar dados!"
            ),
            inline=False,
        )
        embed.set_footer(text="Spy Bot • Estatísticas")
        await message.channel.send(embed=embed)


async def handle_top_command(message):
    """Manipula o comando !top"""
    content = message.content.lower().strip()

    # Determina categoria baseada no comando
    if "voz" in content or "voice" in content:
        category = "voice"
        title = "🎤 Top 10 - Tempo em Voz"
    else:
        category = "online"
        title = "🏆 Top 10 - Tempo Online"

    top_users = get_top_users(10, category)

    if top_users:
        embed = discord.Embed(title=title, color=0x00FF00, timestamp=datetime.now())

        text = ""
        for i, user in enumerate(top_users, 1):
            if category == "online":
                time_str = format_time(timedelta(seconds=user.get("total_online", 0)))
            else:
                time_str = format_time(timedelta(seconds=user.get("total_voice", 0)))

            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            text += f"{medal} **{user.get('name', 'Desconhecido')}**: {time_str}\n"

        embed.description = text
        embed.set_footer(text="Spy Bot • Rankings")
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ Nenhum Dado Encontrado",
            description="Ainda não há dados suficientes para gerar o ranking.",
            color=0xFF0000,
            timestamp=datetime.now(),
        )
        await message.channel.send(embed=embed)


async def handle_achievements_command(message):
    """Manipula o comando !achievements"""

    # Verifica se é para um usuário específico
    if len(message.mentions) > 0:
        target_user = message.mentions[0]
        user_id = str(target_user.id)
        user_name = target_user.display_name
    else:
        target_user = message.author
        user_id = str(target_user.id)
        user_name = target_user.display_name

    achievements = get_user_achievements(user_id)

    if achievements:
        embed = discord.Embed(
            title=f"🏆 Conquistas de {user_name}",
            color=0xFFD700,
            timestamp=datetime.now(),
        )
        embed.set_author(name=user_name, icon_url=target_user.display_avatar.url)

        # Agrupa conquistas por categoria
        categories = {"⏰ Tempo Online": [], "🎤 Voz": [], "🦋 Social": []}

        for achievement in achievements:
            if (
                "hora" in achievement["title"].lower()
                or "dedicado" in achievement["title"].lower()
                or "veterano" in achievement["title"].lower()
            ):
                categories["⏰ Tempo Online"].append(achievement)
            elif (
                "voz" in achievement["title"].lower()
                or "explorador" in achievement["title"].lower()
            ):
                categories["🎤 Voz"].append(achievement)
            else:
                categories["🦋 Social"].append(achievement)

        for category, achievements_list in categories.items():
            if achievements_list:
                text = ""
                for achievement in achievements_list:
                    text += (
                        f"🏆 **{achievement['title']}**: {achievement['description']}\n"
                    )
                embed.add_field(name=category, value=text, inline=False)

        embed.set_footer(text="Spy Bot • Conquistas")
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ Nenhuma Conquista",
            description=f"{user_name} ainda não conquistou nenhuma medalha!",
            color=0xFF0000,
            timestamp=datetime.now(),
        )
        embed.set_author(name=user_name, icon_url=target_user.display_avatar.url)
        await message.channel.send(embed=embed)


async def handle_compare_command(message):
    """Manipula o comando !compare"""
    if len(message.mentions) < 2:
        embed = discord.Embed(
            title="❌ Uso Incorreto",
            description="Use: `!compare @usuario1 @usuario2`",
            color=0xFF0000,
            timestamp=datetime.now(),
        )
        await message.channel.send(embed=embed)
        return

    user1 = message.mentions[0]
    user2 = message.mentions[1]

    user1_data = get_user_data_from_mongodb(str(user1.id))
    user2_data = get_user_data_from_mongodb(str(user2.id))

    if not user1_data or not user2_data:
        embed = discord.Embed(
            title="❌ Dados Insuficientes",
            description=(
                "Um ou ambos os usuários não têm dados suficientes para comparação."
            ),
            color=0xFF0000,
            timestamp=datetime.now(),
        )
        await message.channel.send(embed=embed)
        return

    embed = discord.Embed(
        title="⚖️ Comparação de Usuários",
        description=f"Comparando {user1.display_name} vs {user2.display_name}",
        color=0x0099FF,
        timestamp=datetime.now(),
    )

    # Compara tempo online
    user1_online = user1_data["status_time"].get("online", timedelta())
    user2_online = user2_data["status_time"].get("online", timedelta())

    embed.add_field(
        name="⏰ Tempo Online",
        value=f"**{user1.display_name}**: {format_time(user1_online)}\n"
        f"**{user2.display_name}**: {format_time(user2_online)}",
        inline=True,
    )

    # Compara tempo em voz
    user1_voice = user1_data.get("total_voice_time", timedelta())
    user2_voice = user2_data.get("total_voice_time", timedelta())

    embed.add_field(
        name="🎤 Tempo em Voz",
        value=f"**{user1.display_name}**: {format_time(user1_voice)}\n"
        f"**{user2.display_name}**: {format_time(user2_voice)}",
        inline=True,
    )

    # Compara salas visitadas
    user1_rooms = len(user1_data["voice_time"])
    user2_rooms = len(user2_data["voice_time"])

    embed.add_field(
        name="🏠 Salas Visitadas",
        value=f"**{user1.display_name}**: {user1_rooms} salas\n"
        f"**{user2.display_name}**: {user2_rooms} salas",
        inline=True,
    )

    embed.set_footer(text="Spy Bot • Comparação")
    await message.channel.send(embed=embed)


async def handle_serverstats_command(message):
    """Manipula o comando !serverstats"""
    try:
        # Estatísticas gerais do servidor
        total_users = user_data_collection.count_documents({})

        # Usuários ativos na última semana
        week_ago = datetime.now() - timedelta(days=7)
        active_users = user_data_collection.count_documents(
            {"updated_at": {"$gte": week_ago}}
        )

        # Top 3 usuários online
        top_online = get_top_users(3, "online")

        # Top 3 usuários em voz
        top_voice = get_top_users(3, "voice")

        # Total de conquistas concedidas
        total_achievements = achievements_collection.count_documents({})

        embed = discord.Embed(
            title="📊 Estatísticas do Servidor",
            description=f"Resumo geral da atividade em {message.guild.name}",
            color=0x00FF00,
            timestamp=datetime.now(),
        )

        embed.add_field(
            name="👥 Membros",
            value=(
                f"**Total**: {total_users}\n**Ativos (7d)**: {active_users}\n"
                f"**Taxa**: {round((active_users / total_users * 100), 1)}%"
            ),
            inline=True,
        )

        embed.add_field(
            name="🏆 Conquistas",
            value=f"**Total Concedidas**: {total_achievements}",
            inline=True,
        )

        if top_online:
            online_text = ""
            for i, user in enumerate(top_online, 1):
                time_str = format_time(timedelta(seconds=user.get("total_online", 0)))
                online_text += (
                    f"{i}. **{user.get('name', 'Desconhecido')}**: {time_str}\n"
                )
            embed.add_field(name="🥇 Top 3 - Online", value=online_text, inline=True)

        if top_voice:
            voice_text = ""
            for i, user in enumerate(top_voice, 1):
                time_str = format_time(timedelta(seconds=user.get("total_voice", 0)))
                voice_text += (
                    f"{i}. **{user.get('name', 'Desconhecido')}**: {time_str}\n"
                )
            embed.add_field(name="🎤 Top 3 - Voz", value=voice_text, inline=True)

        embed.set_footer(text="Spy Bot • Estatísticas do Servidor")
        await message.channel.send(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title="❌ Erro",
            description=f"Erro ao gerar estatísticas do servidor: {str(e)}",
            color=0xFF0000,
            timestamp=datetime.now(),
        )
        await message.channel.send(embed=embed)


async def handle_help_command(message):
    """Manipula o comando !help"""
    embed = discord.Embed(
        title="🤖 Spy Bot - Comandos Disponíveis",
        description="Lista completa de todos os comandos e funcionalidades",
        color=0x0099FF,
        timestamp=datetime.now(),
    )

    # Comandos Básicos
    basic_commands = [
        ("!stats", "📊 Mostra suas estatísticas pessoais detalhadas"),
        ("!help", "❓ Mostra esta lista de comandos"),
    ]

    embed.add_field(
        name="🔧 Comandos Básicos",
        value="\n".join([f"**{cmd}** - {desc}" for cmd, desc in basic_commands]),
        inline=False,
    )

    # Comandos de Ranking
    ranking_commands = [
        ("!top", "🏆 Ranking dos 10 membros com mais tempo online"),
        ("!top voz", "🎤 Ranking dos 10 membros com mais tempo em salas de voz"),
    ]

    embed.add_field(
        name="🏆 Comandos de Ranking",
        value="\n".join([f"**{cmd}** - {desc}" for cmd, desc in ranking_commands]),
        inline=False,
    )

    # Comandos de Conquistas
    achievement_commands = [
        ("!achievements", "🏆 Mostra suas conquistas desbloqueadas"),
        ("!achievements @usuario", "🏆 Mostra conquistas de outro usuário"),
    ]

    embed.add_field(
        name="🎖️ Comandos de Conquistas",
        value="\n".join([f"**{cmd}** - {desc}" for cmd, desc in achievement_commands]),
        inline=False,
    )

    # Comandos de Análise
    analysis_commands = [
        ("!compare @user1 @user2", "⚖️ Compara estatísticas de dois usuários"),
        ("!serverstats", "📊 Estatísticas gerais do servidor"),
    ]

    embed.add_field(
        name="📈 Comandos de Análise",
        value="\n".join([f"**{cmd}** - {desc}" for cmd, desc in analysis_commands]),
        inline=False,
    )

    # Informações sobre o bot
    embed.add_field(
        name="🤖 Sobre o Spy Bot",
        value="• **Monitoramento automático** de status e salas de voz\n"
        "• **Sistema de conquistas** baseado em atividade\n"
        "• **Relatórios semanais** automáticos\n"
        "• **Alertas de inatividade** para membros ausentes\n"
        "• **Detecção de plataforma** (Mobile/Desktop)",
        inline=False,
    )

    embed.add_field(
        name="💡 Dica",
        value=(
            "O bot monitora automaticamente sua atividade e concede conquistas "
            "baseadas em suas ações! Use `!stats` para ver seus dados."
        ),
        inline=False,
    )

    embed.set_footer(
        text=(
            "Spy Bot • Sistema de Ajuda • " "Digite !help para ver esta lista novamente"
        )
    )
    await message.channel.send(embed=embed)


async def handle_debug_command(message):
    """Comando de debug para verificar dados (apenas para desenvolvimento)"""
    user_id = str(message.author.id)
    user_data = get_user_data_from_mongodb(user_id)

    if user_data:
        embed = discord.Embed(
            title="🔍 Debug - Dados do Usuário",
            description=f"Dados de {user_data['name']}",
            color=0x0099FF,
            timestamp=datetime.now(),
        )

        # Status times
        status_text = ""
        for status, time in user_data["status_time"].items():
            status_text += f"**{status}**: {format_time(time)}\n"

        embed.add_field(name="⏰ Tempos de Status", value=status_text, inline=True)

        # Current status
        current_status = user_data.get("current_status", "Nenhum")
        status_start = user_data.get("status_start", "Nenhum")

        embed.add_field(
            name="🔄 Status Atual",
            value=f"**Status**: {current_status}\n**Início**: {status_start}",
            inline=True,
        )

        # Voice data
        total_voice = user_data.get("total_voice_time", timedelta())
        embed.add_field(
            name="🎤 Voz",
            value=(
                f"**Total**: {format_time(total_voice)}\n"
                f"**Salas**: {len(user_data['voice_time'])}"
            ),
            inline=True,
        )

        embed.set_footer(text="Spy Bot • Debug")
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ Nenhum Dado Encontrado",
            description="Nenhum dado de debug encontrado para este usuário.",
            color=0xFF0000,
            timestamp=datetime.now(),
        )
        await message.channel.send(embed=embed)


client.run(os.getenv("DISCORD_BOT_TOKEN"))
