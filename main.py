import os
from datetime import datetime, timedelta

import discord
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

CANAL_DE_NOTIFICACAO_ID = int(os.getenv("CANAL_DE_NOTIFICACAO_ID"))
SALA_EXCLUIDA = os.getenv("SALA_EXCLUIDA")

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI, server_api=ServerApi("1"))
db = client.spy_bot
user_data_collection = db.user_data

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.presences = True
intents.voice_states = True

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

        document = {
            "user_id": user_id,
            "name": data["name"],
            "status_time": status_time_seconds,
            "voice_time": voice_time_seconds,
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

            return {
                "name": document["name"],
                "status_time": status_time,
                "voice_time": voice_time,
                "current_status": document["current_status"],
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
            "current_status": new_status,
            "current_voice": None,
            "status_start": datetime.now(),
            "voice_start": None,
        }
    else:
        # Atualiza nome se fornecido
        if member_name:
            user_data["name"] = member_name

        current_time = datetime.now()

        # Calcula tempo do status anterior
        if user_data["current_status"] and user_data["status_start"]:
            elapsed = current_time - user_data["status_start"]
            if user_data["current_status"] in user_data["status_time"]:
                user_data["status_time"][user_data["current_status"]] += elapsed

        # Atualiza para novo status
        user_data["current_status"] = new_status
        user_data["status_start"] = current_time

    # Salva no MongoDB
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
            "current_status": None,
            "current_voice": None,
            "status_start": None,
            "voice_start": None,
        }
    else:
        # Atualiza nome se fornecido
        if member_name:
            user_data["name"] = member_name

    current_time = datetime.now()

    # Processa saída de sala
    if not is_joining and user_data["current_voice"] and user_data["voice_start"]:
        elapsed = current_time - user_data["voice_start"]
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
    return user_data


@client.event
async def on_ready():
    print(f"Bot logado como {client.user} (ID: {client.user.id})")
    print("--------------------------------------------------")
    print("Bot de monitoramento de status e salas de voz está online!")
    print("--------------------------------------------------")

    # Testa conexão com MongoDB
    try:
        client.admin.command("ping")
        print("✅ Conectado com sucesso ao MongoDB!")
    except Exception as e:
        print(f"❌ Erro ao conectar com MongoDB: {e}")

    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="tempo dos membros"
        )
    )


@client.event
async def on_presence_update(before, after):
    if after.bot:
        return

    if before.status != after.status:
        update_status_time(str(after.id), after.status, after.display_name)

        canal_de_notificacao = client.get_channel(CANAL_DE_NOTIFICACAO_ID)

        if not canal_de_notificacao:
            print(
                f"ERRO: Canal de notificação com ID {CANAL_DE_NOTIFICACAO_ID} "
                "não encontrado ou inacessível."
            )
            print(
                "Verifique se o ID está correto e se o bot tem permissão para "
                "ver e enviar mensagens no canal."
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

        if before.status == discord.Status.offline:
            return

        mensagem = ""

        if after.status == discord.Status.online:
            mensagem = f"**{after.display_name}** está **{status_atual_nome}**!"
        elif after.status == discord.Status.offline:
            mensagem = f"**{after.display_name}** ficou **{status_atual_nome}**."
        elif after.status == discord.Status.idle:
            mensagem = (
                f"**{after.display_name}** está **{status_atual_nome}** " "(Ausente)."
            )
        elif after.status == discord.Status.dnd:
            mensagem = (
                f"**{after.display_name}** está **{status_atual_nome}** "
                "(Não Incomodar)."
            )
        else:
            mensagem = (
                f"**{after.display_name}** mudou de status: de "
                f"{status_anterior_nome} para {status_atual_nome}."
            )

        if mensagem:
            embed = discord.Embed(
                title="🔄 Mudança de Status",
                description=mensagem,
                color=(
                    0x00FF00
                    if after.status == discord.Status.online
                    else (
                        0xFF0000
                        if after.status == discord.Status.dnd
                        else (
                            0xFFFF00
                            if after.status == discord.Status.idle
                            else 0x808080
                        )
                    )
                ),
                timestamp=datetime.now(),
            )
            embed.set_author(name=after.display_name, icon_url=after.display_avatar.url)
            embed.set_footer(text="Spy Bot • Monitoramento de Status")
            await canal_de_notificacao.send(embed=embed)


@client.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    user_id = str(member.id)

    if before.channel is None and after.channel is not None:
        channel_name = after.channel.name
        if channel_name != SALA_EXCLUIDA:
            update_voice_time(user_id, channel_name, True, member.display_name)

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
        if channel_name != SALA_EXCLUIDA:
            user_data = update_voice_time(
                user_id, channel_name, False, member.display_name
            )

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

        if old_channel != SALA_EXCLUIDA:
            update_voice_time(user_id, old_channel, False, member.display_name)

        if new_channel != SALA_EXCLUIDA:
            update_voice_time(user_id, new_channel, True, member.display_name)

        canal_de_notificacao = client.get_channel(CANAL_DE_NOTIFICACAO_ID)
        if canal_de_notificacao:
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
            elif old_channel == SALA_EXCLUIDA:
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
            elif new_channel == SALA_EXCLUIDA:
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


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!stats"):
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
            embed.set_author(
                name=user["name"], icon_url=message.author.display_avatar.url
            )

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

            # Tempo em Salas de Voz
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
                ):
                    current_time = datetime.now() - user["voice_start"]
                    voice_text += (
                        f"🎤 **{user['current_voice']}**: "
                        f"{format_time(current_time)} *(atual)*\n"
                    )

                embed.add_field(
                    name="🎤 Tempo em Salas de Voz", value=voice_text, inline=False
                )
            else:
                embed.add_field(
                    name="🎤 Tempo em Salas de Voz",
                    value="*Nenhuma sala visitada ainda*",
                    inline=False,
                )

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


client.run(os.getenv("DISCORD_BOT_TOKEN"))
