import asyncio
from datetime import datetime

import discord

from services.user_service import UserService
from utils.formatters import format_time


class AdminCommands:
    @staticmethod
    async def handle_debug(message):
        user_id = str(message.author.id)
        user_data = UserService.get_user_data(user_id)

        if user_data:
            embed = discord.Embed(
                title="🔍 Debug - Dados do Usuário",
                description=f"Dados de {user_data.name}",
                color=0x0099FF,
                timestamp=datetime.now(),
            )

            status_text = ""
            for status, time in user_data.status_time.items():
                status_text += f"**{status}**: {format_time(time)}\n"

            embed.add_field(name="⏰ Tempos de Status", value=status_text, inline=True)

            current_status = user_data.current_status or "Nenhum"
            status_start = user_data.status_start or "Nenhum"

            embed.add_field(
                name="🔄 Status Atual",
                value=f"**Status**: {current_status}\n**Início**: {status_start}",
                inline=True,
            )

            total_voice = user_data.total_voice_time
            embed.add_field(
                name="🎤 Voz",
                value=f"**Total**: {format_time(total_voice)}\n**Salas**: {len(user_data.voice_time)}",
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

    @staticmethod
    async def handle_clear(message):
        if not message.author.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="❌ Permissão Negada",
                description=(
                    "Você precisa ter a permissão 'Gerenciar Mensagens' "
                    "para usar este comando."
                ),
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(text="Spy Bot • Comando Clear")
            await message.channel.send(embed=embed)
            return

        try:
            embed = discord.Embed(
                title="🧹 Limpando Canal",
                description="Iniciando limpeza de todas as mensagens...",
                color=0x00FF00,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(text="Spy Bot • Comando Clear")
            await message.channel.send(embed=embed)

            deleted_count = 0

            async for msg in message.channel.history(limit=None):
                try:
                    await msg.delete()
                    deleted_count += 1
                except discord.Forbidden:
                    continue
                except discord.HTTPException:
                    continue

            success_embed = discord.Embed(
                title="✅ Canal Limpo",
                description=(
                    f"**{deleted_count}** mensagens foram removidas do canal.\n\n"
                    "⏰ Esta mensagem será removida em 30 segundos e o comando de "
                    "ajuda será exibido."
                ),
                color=0x00FF00,
                timestamp=datetime.now(),
            )
            success_embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            success_embed.set_footer(text="Spy Bot • Comando Clear")
            success_msg = await message.channel.send(embed=success_embed)

            await asyncio.sleep(30)

            try:
                await success_msg.delete()
            except discord.HTTPException:
                pass

            from commands.help_command import HelpCommand

            await HelpCommand.handle(message)

        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Erro ao Limpar Canal",
                description=f"Ocorreu um erro durante a limpeza: {str(e)}",
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            error_embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            error_embed.set_footer(text="Spy Bot • Comando Clear")
            await message.channel.send(embed=error_embed)
