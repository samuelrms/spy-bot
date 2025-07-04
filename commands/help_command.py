from datetime import datetime

import discord


class HelpCommand:
    @staticmethod
    async def handle(message):
        embed = discord.Embed(
            title="🤖 Spy Bot - Comandos Disponíveis",
            description="Lista completa de todos os comandos e funcionalidades",
            color=0x0099FF,
            timestamp=datetime.now(),
        )

        basic_commands = [
            ("!stats", "📊 Mostra suas estatísticas pessoais detalhadas"),
            ("!help", "❓ Mostra esta lista de comandos"),
            ("!clear", "🧹 Limpa todas as mensagens do canal atual (requer permissão)"),
        ]

        embed.add_field(
            name="🔧 Comandos Básicos",
            value="\n".join([f"**{cmd}** - {desc}" for cmd, desc in basic_commands]),
            inline=False,
        )

        ranking_commands = [
            ("!top", "🏆 Ranking dos 10 membros com mais tempo online"),
            ("!top voz", "🎤 Ranking dos 10 membros com mais tempo em salas de voz"),
        ]

        embed.add_field(
            name="🏆 Comandos de Ranking",
            value="\n".join([f"**{cmd}** - {desc}" for cmd, desc in ranking_commands]),
            inline=False,
        )

        achievement_commands = [
            ("!achievements", "🏆 Mostra suas conquistas desbloqueadas"),
            ("!achievements @usuario", "🏆 Mostra conquistas de outro usuário"),
            (
                "!achievements-categories",
                "🏆 Mostra todas as categorias de conquistas (50 total!)",
            ),
        ]

        embed.add_field(
            name="🎖️ Comandos de Conquistas",
            value="\n".join(
                [f"**{cmd}** - {desc}" for cmd, desc in achievement_commands]
            ),
            inline=False,
        )

        analysis_commands = [
            ("!compare @user1 @user2", "⚖️ Compara estatísticas de dois usuários"),
            ("!serverstats", "📊 Estatísticas gerais do servidor"),
        ]

        silence_commands = [
            (
                "!silence",
                "🔇 Mostra um tutorial de como silenciar o canal manualmente pelo Discord (via DM)",
            ),
        ]

        sleep_commands = [
            ("!sleep", "😴 Ativa o modo silencioso do bot (só responde comandos)"),
            ("!sleep 30m", "😴 Ativa modo silencioso por 30 minutos"),
            ("!sleep 2h", "😴 Ativa modo silencioso por 2 horas"),
            ("!sleep 1d", "😴 Ativa modo silencioso por 1 dia"),
            ("!wake", "🌅 Desativa o modo silencioso do bot"),
            ("!status-sleep", "📊 Mostra o status atual do modo silencioso"),
        ]

        embed.add_field(
            name="📈 Comandos de Análise",
            value="\n".join([f"**{cmd}** - {desc}" for cmd, desc in analysis_commands]),
            inline=False,
        )

        embed.add_field(
            name="🔇 Comandos de Silenciamento",
            value="\n".join([f"**{cmd}** - {desc}" for cmd, desc in silence_commands]),
            inline=False,
        )

        embed.add_field(
            name="😴 Comandos de Modo Silencioso",
            value="\n".join([f"**{cmd}** - {desc}" for cmd, desc in sleep_commands]),
            inline=False,
        )

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
            value="O bot monitora automaticamente sua atividade e concede conquistas baseadas em suas ações! Use `!stats` para ver seus dados.",
            inline=False,
        )

        embed.set_footer(
            text="Spy Bot • Sistema de Ajuda • Digite !help para ver esta lista novamente"
        )
        await message.channel.send(embed=embed)

    @staticmethod
    async def handle_silence(message):
        embed = discord.Embed(
            title="🔇 Como silenciar este canal no Discord",
            description="Para não receber notificações deste canal:\n"
            "1. Clique com o botão direito no canal desejado.\n"
            "2. Selecione 'Silenciar canal'.\n"
            "3. Escolha o tempo desejado ou 'Até eu ligar de novo'.\n\n"
            "Isso é uma configuração pessoal e não afeta outros membros.",
            color=0x0099FF,
            timestamp=datetime.now(),
        )
        embed.set_footer(
            text="Dica: Você pode reverter isso a qualquer momento pelo mesmo menu."
        )
        try:
            await message.author.send(embed=embed)
            if message.guild:
                await message.add_reaction("📬")
        except Exception:
            await message.channel.send(embed=embed)
