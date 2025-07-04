import re
from datetime import datetime

import discord

from services.sleep_service import SleepService


class SleepCommand:
    @staticmethod
    async def handle_sleep(message):
        content = message.content.strip()
        match = re.match(r"!sleep(?:\s+(\d+)([mhd]))?", content)

        if match:
            if match.group(1) and match.group(2):
                value = int(match.group(1))
                unit = match.group(2)
                seconds = (
                    value * 60
                    if unit == "m"
                    else value * 3600
                    if unit == "h"
                    else value * 86400
                )
                SleepService.sleep(seconds)

                embed = discord.Embed(
                    title="😴 SPY BOT Dormindo",
                    description=(
                        f"**Tempo**: {value}{unit}\n"
                        f"**Acorda**: Com `!wake` ou após {value}{unit}"
                    ),
                    color=0x9B59B6,
                    timestamp=datetime.now(),
                )
                embed.set_author(
                    name=message.author.display_name,
                    icon_url=message.author.display_avatar.url,
                )
                embed.set_footer(text="Spy Bot • Modo Silencioso")
                await message.channel.send(embed=embed)
            else:
                SleepService.sleep()

                embed = discord.Embed(
                    title="�� SPY BOT Dormindo",
                    description="**Modo**: Indefinido\n**Acorda**: Com `!wake`",
                    color=0x9B59B6,
                    timestamp=datetime.now(),
                )
                embed.set_author(
                    name=message.author.display_name,
                    icon_url=message.author.display_avatar.url,
                )
                embed.set_footer(text="Spy Bot • Modo Silencioso")
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Uso Incorreto",
                description=(
                    "**Formato**: `!sleep [tempo]`\n\n**Exemplos**:\n"
                    "• `!sleep` - Dorme indefinidamente\n"
                    "• `!sleep 30m` - Dorme por 30 minutos\n"
                    "• `!sleep 2h` - Dorme por 2 horas\n"
                    "• `!sleep 1d` - Dorme por 1 dia"
                ),
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(text="Spy Bot • Modo Silencioso")
            await message.channel.send(embed=embed)

    @staticmethod
    async def handle_wake(message):
        SleepService.wake()

        embed = discord.Embed(
            title="☀️ SPY BOT Acordou!",
            description="**Status**: Ativo\n**Funcionalidades**: Todas restauradas\n**Monitoramento**: Normal",
            color=0x00FF00,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name=message.author.display_name, icon_url=message.author.display_avatar.url
        )
        embed.set_footer(text="Spy Bot • Modo Silencioso")
        await message.channel.send(embed=embed)

    @staticmethod
    async def handle_status(message):
        from datetime import datetime

        from services.sleep_service import SleepService

        now = datetime.now()
        manual = SleepService._manual_sleep
        until = SleepService._sleep_until

        if manual:
            desc = (
                "😴 O bot está dormindo **indefinidamente**!\n"
                "Acorda apenas com o comando `!wake`.\n\n"
                "Aproveite o silêncio... ou acorde o bot para voltar à ação!"
            )
        elif until and now < until:
            restante = until - now
            total_seconds = int(restante.total_seconds())
            horas, resto = divmod(total_seconds, 3600)
            minutos, segundos = divmod(resto, 60)
            desc = (
                f"⏳ O bot está dormindo por tempo limitado!\n"
                f"**Acorda em:** {horas}h {minutos}m {segundos}s (ou com `!wake`)\n\n"
                f"Fique de olho, logo ele volta à ativa!"
            )
        else:
            desc = "☀️ O bot está **acordado** e monitorando tudo normalmente!\n\nUse `!sleep` para ativar o modo silencioso."

        embed = discord.Embed(
            title="🛌 Status do SPY BOT", description=desc, color=0x0099FF, timestamp=now
        )
        embed.set_author(
            name=message.author.display_name, icon_url=message.author.display_avatar.url
        )
        embed.set_footer(text="Spy Bot • Modo Silencioso")
        await message.channel.send(embed=embed)
