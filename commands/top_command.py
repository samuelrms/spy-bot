from datetime import datetime

import discord


class TopCommand:
    @staticmethod
    async def handle(message):
        try:
            content = message.content.lower().strip()

            if "voz" in content:
                await TopCommand.show_voice_ranking(message)
            else:
                await TopCommand.show_general_ranking(message)

        except Exception as e:
            print(f"❌ Erro no comando !top: {e}")
            embed = discord.Embed(
                title="❌ Erro",
                description="Erro ao gerar ranking. Tente novamente mais tarde.",
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(text="Spy Bot • Ranking")
            await message.channel.send(embed=embed)

    @staticmethod
    async def show_general_ranking(message):
        """Mostra ranking geral de atividade"""
        try:
            embed = discord.Embed(
                title="🏆 Ranking de Atividade",
                description="Top 10 membros mais ativos",
                color=0x0099FF,
                timestamp=datetime.now(),
            )

            rankings = [
                ("🥇 Usuario1", "💬 150 mensagens • 🎤 5h 30m"),
                ("🥈 Usuario2", "💬 120 mensagens • 🎤 4h 15m"),
                ("🥉 Usuario3", "💬 95 mensagens • 🎤 3h 45m"),
                ("4️⃣ Usuario4", "💬 80 mensagens • 🎤 2h 30m"),
                ("5️⃣ Usuario5", "💬 65 mensagens • 🎤 2h 15m"),
                ("6️⃣ Usuario6", "💬 55 mensagens • 🎤 1h 45m"),
                ("7️⃣ Usuario7", "💬 45 mensagens • 🎤 1h 30m"),
                ("8️⃣ Usuario8", "💬 40 mensagens • 🎤 1h 15m"),
                ("9️⃣ Usuario9", "💬 35 mensagens • 🎤 1h 00m"),
                ("🔟 Usuario10", "💬 30 mensagens • 🎤 45m"),
            ]

            ranking_text = "\n".join(
                [f"**{name}**\n{stats}" for name, stats in rankings]
            )

            embed.add_field(name="📊 Ranking Geral", value=ranking_text, inline=False)

            embed.add_field(
                name="⚠️ Aviso",
                value="Dados de exemplo (MongoDB não disponível)",
                inline=False,
            )

            embed.set_footer(text="Spy Bot • Ranking de Atividade")

            await message.channel.send(embed=embed)

        except Exception as e:
            print(f"❌ Erro no ranking geral: {e}")
            embed = discord.Embed(
                title="❌ Erro",
                description="Erro ao gerar ranking geral. Tente novamente mais tarde.",
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(text="Spy Bot • Ranking Geral")
            await message.channel.send(embed=embed)

    @staticmethod
    async def show_voice_ranking(message):
        """Mostra ranking de tempo em voz"""
        try:
            embed = discord.Embed(
                title="🎤 Ranking de Tempo em Voz",
                description="Top 10 membros com mais tempo em salas de voz",
                color=0x0099FF,
                timestamp=datetime.now(),
            )

            voice_rankings = [
                ("🥇 VozUser1", "🎤 8h 30m • 🏠 5 salas"),
                ("🥈 VozUser2", "🎤 6h 45m • 🏠 3 salas"),
                ("🥉 VozUser3", "🎤 5h 20m • 🏠 4 salas"),
                ("4️⃣ VozUser4", "🎤 4h 15m • 🏠 2 salas"),
                ("5️⃣ VozUser5", "🎤 3h 30m • 🏠 3 salas"),
                ("6️⃣ VozUser6", "🎤 2h 45m • 🏠 2 salas"),
                ("7️⃣ VozUser7", "🎤 2h 15m • 🏠 1 sala"),
                ("8️⃣ VozUser8", "🎤 1h 50m • 🏠 2 salas"),
                ("9️⃣ VozUser9", "🎤 1h 30m • 🏠 1 sala"),
                ("🔟 VozUser10", "🎤 1h 15m • 🏠 1 sala"),
            ]

            voice_text = "\n".join(
                [f"**{name}**\n{stats}" for name, stats in voice_rankings]
            )

            embed.add_field(name="🎤 Tempo em Voz", value=voice_text, inline=False)

            embed.add_field(
                name="⚠️ Aviso",
                value="Dados de exemplo (MongoDB não disponível)",
                inline=False,
            )

            embed.set_footer(text="Spy Bot • Ranking de Voz")

            await message.channel.send(embed=embed)

        except Exception as e:
            print(f"❌ Erro no ranking de voz: {e}")
            embed = discord.Embed(
                title="❌ Erro",
                description="Erro ao gerar ranking de voz. Tente novamente mais tarde.",
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(text="Spy Bot • Ranking de Voz")
            await message.channel.send(embed=embed)
