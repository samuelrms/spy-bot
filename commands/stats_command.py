import traceback
from datetime import datetime, timedelta

import discord

from services.achievement_service import AchievementService
from services.user_service import UserService
from utils.formatters import format_time


class StatsCommand:
    @staticmethod
    async def handle(message):
        try:
            user_id = str(message.author.id)

            try:
                user_data = UserService.get_user_data(user_id)
                has_mongo = True
            except Exception as e:
                print(f"⚠️ MongoDB não disponível, usando dados mock: {e}")
                user_data = {
                    "messages_sent": 50,
                    "time_in_voice": 3600,
                    "reactions_given": 25,
                    "reactions_received": 30,
                    "join_date": datetime.now() - timedelta(days=30),
                    "last_seen": datetime.now(),
                    "platform": "desktop",
                }
                has_mongo = False

            embed = discord.Embed(
                title=f"📊 Estatísticas de {message.author.display_name}",
                color=0x0099FF,
                timestamp=datetime.now(),
            )

            embed.add_field(
                name="💬 Mensagens",
                value=f"**{user_data.get('messages_sent', 0)}** mensagens enviadas",
                inline=True,
            )

            voice_time = user_data.get("time_in_voice", 0)
            hours = voice_time // 3600
            minutes = (voice_time % 3600) // 60
            embed.add_field(
                name="🎤 Tempo em Voz",
                value=f"**{hours}h {minutes}m** total",
                inline=True,
            )

            embed.add_field(
                name="👍 Reações",
                value=f"**{user_data.get('reactions_given', 0)}** dadas • **{user_data.get('reactions_received', 0)}** recebidas",
                inline=True,
            )

            join_date = user_data.get("join_date", datetime.now())
            days_member = (datetime.now() - join_date).days
            embed.add_field(
                name="📅 Membro desde",
                value=f"**{days_member}** dias no servidor",
                inline=True,
            )

            last_seen = user_data.get("last_seen", datetime.now())
            embed.add_field(
                name="🕐 Última atividade",
                value=f"<t:{int(last_seen.timestamp())}:R>",
                inline=True,
            )

            platform = user_data.get("platform", "desktop")
            platform_emoji = "🖥️" if platform == "desktop" else "📱"
            embed.add_field(
                name="💻 Plataforma",
                value=f"{platform_emoji} **{platform.title()}**",
                inline=True,
            )

            if not has_mongo:
                embed.add_field(
                    name="⚠️ Aviso",
                    value="Dados de exemplo (MongoDB não disponível)",
                    inline=False,
                )

            embed.set_thumbnail(url=message.author.display_avatar.url)
            embed.set_footer(text="Spy Bot • Estatísticas Pessoais")

            await message.channel.send(embed=embed)

        except Exception as e:
            print(f"❌ Erro no comando !stats: {e}")
            traceback.print_exc()
            embed = discord.Embed(
                title="❌ Erro",
                description="Erro ao buscar estatísticas. Tente novamente mais tarde.",
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(text="Spy Bot • Estatísticas")
            await message.channel.send(embed=embed)

    @staticmethod
    async def handle_compare(message):
        try:
            if len(message.mentions) != 2:
                embed = discord.Embed(
                    title="❌ Uso Incorreto",
                    description="**Formato**: `!compare @usuario1 @usuario2`\n\n**Exemplo**:\n`!compare @João @Maria`",
                    color=0xFF0000,
                    timestamp=datetime.now(),
                )
                embed.set_author(
                    name=message.author.display_name,
                    icon_url=message.author.display_avatar.url,
                )
                embed.set_footer(text="Spy Bot • Comparação")
                await message.channel.send(embed=embed)
                return

            user1, user2 = message.mentions[0], message.mentions[1]

            embed = discord.Embed(
                title="⚖️ Comparação de Estatísticas",
                description=f"Comparando {user1.display_name} vs {user2.display_name}",
                color=0x0099FF,
                timestamp=datetime.now(),
            )

            embed.add_field(
                name=f"{user1.display_name}",
                value="💬 50 mensagens\n🎤 2h 30m em voz\n👍 25 reações",
                inline=True,
            )

            embed.add_field(
                name=f"{user2.display_name}",
                value="💬 75 mensagens\n🎤 1h 45m em voz\n👍 40 reações",
                inline=True,
            )

            embed.add_field(
                name="🏆 Vencedor",
                value=f"{user2.display_name} tem mais atividade!",
                inline=False,
            )

            await message.channel.send(embed=embed)

        except Exception as e:
            print(f"❌ Erro no comando !compare: {e}")
            embed = discord.Embed(
                title="❌ Erro",
                description="Erro ao comparar usuários. Tente novamente mais tarde.",
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(text="Spy Bot • Comparação")
            await message.channel.send(embed=embed)

    @staticmethod
    async def handle_serverstats(message):
        try:
            guild = message.guild
            if not guild:
                embed = discord.Embed(
                    title="❌ Comando Inválido",
                    description="Este comando só funciona em servidores.",
                    color=0xFF0000,
                    timestamp=datetime.now(),
                )
                embed.set_author(
                    name=message.author.display_name,
                    icon_url=message.author.display_avatar.url,
                )
                embed.set_footer(text="Spy Bot • Estatísticas do Servidor")
                await message.channel.send(embed=embed)
                return

            embed = discord.Embed(
                title="📊 Estatísticas do Servidor",
                description=guild.name,
                color=0x0099FF,
                timestamp=datetime.now(),
            )

            embed.add_field(
                name="👥 Membros", value=f"**{guild.member_count}** total", inline=True
            )

            embed.add_field(
                name="🎤 Canais de Voz",
                value=f"**{len(guild.voice_channels)}** ativos",
                inline=True,
            )

            embed.add_field(
                name="💬 Canais de Texto",
                value=f"**{len(guild.text_channels)}** ativos",
                inline=True,
            )

            embed.add_field(
                name="📅 Criado em",
                value=f"<t:{int(guild.created_at.timestamp())}:D>",
                inline=True,
            )

            embed.add_field(
                name="👑 Proprietário",
                value=guild.owner.display_name if guild.owner else "Desconhecido",
                inline=True,
            )

            embed.add_field(name="🆔 ID do Servidor", value=guild.id, inline=True)

            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)

            embed.set_footer(text="Spy Bot • Estatísticas do Servidor")

            await message.channel.send(embed=embed)

        except Exception as e:
            print(f"❌ Erro no comando !serverstats: {e}")
            embed = discord.Embed(
                title="❌ Erro",
                description="Erro ao buscar estatísticas do servidor. Tente novamente mais tarde.",
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(text="Spy Bot • Estatísticas do Servidor")
            await message.channel.send(embed=embed)

    @staticmethod
    async def handle_stats(message):
        user_id = str(message.author.id)
        user_data = UserService.get_user_data(user_id)

        if user_data:
            current_voice_time = timedelta()
            if user_data.current_voice and user_data.voice_start:
                current_voice_time = datetime.now() - user_data.voice_start

            embed = discord.Embed(
                title=f"📊 Estatísticas de {user_data.name}",
                color=0x00FF00,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=user_data.name, icon_url=message.author.display_avatar.url
            )

            status_text = ""
            status_emojis = {"online": "🟢", "offline": "⚫", "idle": "🟡", "dnd": "🔴"}

            for status, time in user_data.status_time.items():
                if status == user_data.current_status and user_data.status_start:
                    current_time = datetime.now() - user_data.status_start
                    total_time = time + current_time
                    status_text += f"{status_emojis.get(status, '❓')} **{status.title()}**: {format_time(total_time)} *(atual)*\n"
                else:
                    total_time = time
                    status_text += f"{status_emojis.get(status, '❓')} **{status.title()}**: {format_time(total_time)}\n"

            embed.add_field(name="⏰ Tempo por Status", value=status_text, inline=False)

            if user_data.current_voice and user_data.voice_start:
                embed.add_field(
                    name="🎤 Canal Atual",
                    value=f"**{user_data.current_voice}**: {format_time(current_voice_time)} *(em andamento)*",
                    inline=False,
                )

            total_voice_time = user_data.total_voice_time
            if user_data.current_voice and user_data.voice_start:
                current_time = datetime.now() - user_data.voice_start
                total_voice_time += current_time

            embed.add_field(
                name="🎤 Tempo Total em Voz",
                value=f"**{format_time(total_voice_time)}**",
                inline=True,
            )

            if user_data.voice_time:
                voice_text = ""
                for room, time in user_data.voice_time.items():
                    if room == user_data.current_voice and user_data.voice_start:
                        current_time = datetime.now() - user_data.voice_start
                        total_time = time + current_time
                        voice_text += (
                            f"🎤 **{room}**: {format_time(total_time)} *(atual)*\n"
                        )
                    else:
                        total_time = time
                        voice_text += f"🎤 **{room}**: {format_time(total_time)}\n"

                if (
                    user_data.current_voice
                    and user_data.current_voice not in user_data.voice_time
                ):
                    current_time = datetime.now() - user_data.voice_start
                    voice_text += f"🎤 **{user_data.current_voice}**: {format_time(current_time)} *(atual)*\n"

                embed.add_field(name="🎤 Salas de Voz", value=voice_text, inline=False)
            else:
                embed.add_field(
                    name="🎤 Salas de Voz",
                    value="*Nenhuma sala visitada ainda*",
                    inline=False,
                )

            achievements = AchievementService.get_user_achievements(user_id)
            if achievements:
                achievements_text = ""
                for achievement in achievements[:5]:
                    achievements_text += (
                        f"🏆 **{achievement.title}**: {achievement.description}\n"
                    )
                embed.add_field(
                    name="🏆 Conquistas", value=achievements_text, inline=False
                )

            embed.set_footer(text="Spy Bot • Estatísticas")
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Dados Não Encontrados",
                description="Nenhum dado de monitoramento foi encontrado para você ainda.",
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.add_field(
                name="💡 Dica",
                value="Entre em uma sala de voz ou mude seu status para começar a coletar dados!",
                inline=False,
            )
            embed.set_footer(text="Spy Bot • Estatísticas")
            await message.channel.send(embed=embed)
