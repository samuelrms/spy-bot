from datetime import datetime

import discord


class AchievementsCommand:
    @staticmethod
    async def handle(message):
        try:
            if message.mentions:
                target_user = message.mentions[0]
                user_id = str(target_user.id)
                user_name = target_user.display_name
            else:
                target_user = message.author
                user_id = str(message.author.id)
                user_name = message.author.display_name

            await AchievementsCommand.show_achievements(
                message, user_id, user_name, target_user
            )

        except Exception as e:
            print(f"❌ Erro no comando !achievements: {e}")
            embed = discord.Embed(
                title="❌ Erro",
                description="Erro ao buscar conquistas. Tente novamente mais tarde.",
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(text="Spy Bot • Sistema de Conquistas")
            await message.channel.send(embed=embed)

    @staticmethod
    async def handle_categories(message):
        try:
            embed = discord.Embed(
                title="🏆 CATEGORIAS DE CONQUISTAS - VOCÊ CONSEGUE PEGAR TODAS?",
                description=(
                    "**50 CONQUISTAS ESPERANDO POR VOCÊ!** 🎯\n\n"
                    "*Será que você tem o que é preciso para se tornar uma "
                    "**LENDA DO DISCORD**?* 😈"
                ),
                color=0xFFD700,
                timestamp=datetime.now(),
            )

            categories = [
                {
                    "name": "🎤 Voz & Presença",
                    "count": 8,
                    "description": (
                        "**OS MAIS SOCIÁVEIS** - Quem fica mais tempo em call? "
                        "Será você?"
                    ),
                    "challenge": "Conseguirá ficar 24h seguidas em voz? 😏",
                },
                {
                    "name": "💬 Mensagens & Reações",
                    "count": 12,
                    "description": "**OS MAIS ATIVOS** - Tagarela ou comunicador?",
                    "challenge": "1000 mensagens em um dia? Vamos ver! 💪",
                },
                {
                    "name": "🦋 Social & Comunidade",
                    "count": 7,
                    "description": (
                        "**OS MAIS POPULARES** - Quem é o coração da comunidade?"
                    ),
                    "challenge": "Será que você consegue ajudar 50 pessoas? 🤝",
                },
                {
                    "name": "📈 Engajamento & Uso",
                    "count": 6,
                    "description": "**OS MAIS DEDICADOS** - Viciado em Discord?",
                    "challenge": "7 dias seguidos online? Sem dormir? 😴",
                },
                {
                    "name": "⏰ Atividade & Consistência",
                    "count": 5,
                    "description": (
                        "**OS MAIS PERSISTENTES** - Consegue manter o ritmo?"
                    ),
                    "challenge": "30 dias seguidos ativo? Vamos lá! ⏰",
                },
                {
                    "name": "🎲 Diversão & Extras",
                    "count": 8,
                    "description": "**OS MAIS CRIATIVOS** - Quem tem mais estilo?",
                    "challenge": "Usar todos os emojis personalizados? 🎨",
                },
                {
                    "name": "🌙 Lunático do Discord",
                    "count": 4,
                    "description": "**OS MAIS LOUCOS** - Madrugador ou insone?",
                    "challenge": "Ficar online das 2h às 6h por 7 dias? 🌙",
                },
            ]

            total_achievements = sum(cat["count"] for cat in categories)

            for category in categories:
                embed.add_field(
                    name=f"{category['name']} ({category['count']} conquistas)",
                    value=(
                        f"{category['description']}\n"
                        f"**Desafio:** {category['challenge']}"
                    ),
                    inline=False,
                )

            embed.add_field(
                name="📊 ESTATÍSTICAS GLOBAIS",
                value=(
                    f"**Total de Conquistas:** {total_achievements}\n"
                    f"**Conquistas Raras:** 15 (só para os melhores!)\n"
                    f"**Conquistas Secretas:** 5 (você vai descobrir?)\n"
                    f"**Conquista Suprema:** 1 (apenas para LENDAS!)"
                ),
                inline=False,
            )

            embed.add_field(
                name="🔥 DESAFIO FINAL",
                value=(
                    "**CONSIGA TODAS AS 50 CONQUISTAS E SE TORNE UMA LENDA!**\n"
                    "Menos de 1% dos usuários conseguem isso...\n"
                    "**Será que você é digno?** 👑"
                ),
                inline=False,
            )

            embed.add_field(
                name="💡 DICAS PARA SE TORNAR UMA LENDA",
                value=(
                    "• **Seja ativo todos os dias** - Consistência é chave!\n"
                    "• **Interaja com a comunidade** - Faça amigos!\n"
                    "• **Explore todas as funcionalidades** - Seja curioso!\n"
                    "• **Ajude outros membros** - Seja útil!\n"
                    "• **Não desista** - Lendas não desistem!"
                ),
                inline=False,
            )

            embed.set_footer(text="🏆 Spy Bot • Sistema de Conquistas • Desafie-se!")

            await message.channel.send(embed=embed)

        except Exception as e:
            print(f"❌ Erro no comando !achievements-categories: {e}")
            embed = discord.Embed(
                title="❌ Erro",
                description=(
                    "Erro ao mostrar categorias de conquistas. "
                    "Tente novamente mais tarde."
                ),
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(text="Spy Bot • Sistema de Conquistas")
            await message.channel.send(embed=embed)

    @staticmethod
    async def show_achievements(message, user_id, user_name, target_user):
        try:
            embed = discord.Embed(
                title=f"🏆 Conquistas de {user_name}",
                description="Conquistas desbloqueadas baseadas em atividade",
                color=0x0099FF,
                timestamp=datetime.now(),
            )

            try:
                from services.achievement_service import AchievementService

                achievements = AchievementService.get_user_achievements(user_id)
                has_mongo = True
            except Exception as e:
                print(f"⚠️ MongoDB não disponível, usando conquistas mock: {e}")
                achievements = [
                    {
                        "id": "chatterbox",
                        "name": "💬 Tagarela",
                        "description": "100 mensagens enviadas",
                        "unlocked_at": datetime.now(),
                    },
                    {
                        "id": "voice_explorer",
                        "name": "🎤 Explorador de Voz",
                        "description": "Visitou 5 salas de voz diferentes",
                        "unlocked_at": datetime.now(),
                    },
                    {
                        "id": "reaction_master",
                        "name": "👍 Mestre das Reações",
                        "description": "Deu 50 reações",
                        "unlocked_at": datetime.now(),
                    },
                ]
                has_mongo = False

            if achievements:
                categories = {
                    "🎤 Voz & Presença": [],
                    "💬 Mensagens & Reações": [],
                    "🦋 Social & Comunidade": [],
                    "📈 Engajamento & Uso": [],
                    "⏰ Atividade & Consistência": [],
                    "🎲 Diversão & Extras": [],
                    "🌙 Lunático do Discord": [],
                }

                for achievement in achievements:
                    if "voice" in achievement["id"] or "voz" in achievement["id"]:
                        categories["🎤 Voz & Presença"].append(achievement)
                    elif (
                        "message" in achievement["id"]
                        or "reaction" in achievement["id"]
                    ):
                        categories["💬 Mensagens & Reações"].append(achievement)
                    elif (
                        "social" in achievement["id"]
                        or "community" in achievement["id"]
                    ):
                        categories["🦋 Social & Comunidade"].append(achievement)
                    elif (
                        "engagement" in achievement["id"] or "use" in achievement["id"]
                    ):
                        categories["📈 Engajamento & Uso"].append(achievement)
                    elif (
                        "activity" in achievement["id"]
                        or "consistency" in achievement["id"]
                    ):
                        categories["⏰ Atividade & Consistência"].append(achievement)
                    elif "fun" in achievement["id"] or "extra" in achievement["id"]:
                        categories["🎲 Diversão & Extras"].append(achievement)
                    elif "lunatic" in achievement["id"] or "night" in achievement["id"]:
                        categories["🌙 Lunático do Discord"].append(achievement)
                    else:
                        categories["📈 Engajamento & Uso"].append(achievement)

                for category, category_achievements in categories.items():
                    if category_achievements:
                        achievement_text = ""
                        for achievement in category_achievements:
                            unlock_date = achievement.get("unlocked_at", datetime.now())
                            achievement_text += (
                                f"**{achievement['name']}**\n"
                                f"{achievement['description']}\n"
                                f"<t:{int(unlock_date.timestamp())}:R>\n\n"
                            )

                        embed.add_field(
                            name=category, value=achievement_text.strip(), inline=False
                        )

                total_achievements = len(achievements)
                embed.add_field(
                    name="📊 Estatísticas",
                    value=(
                        f"**Total de Conquistas**: {total_achievements}\n"
                        f"**Progresso**: {total_achievements}/50 conquistas"
                    ),
                    inline=False,
                )

            else:
                embed.add_field(
                    name="❌ Nenhuma Conquista",
                    value=(
                        "Este usuário ainda não desbloqueou nenhuma conquista.\n"
                        "Continue ativo para ganhar conquistas!"
                    ),
                    inline=False,
                )

            if not has_mongo:
                embed.add_field(
                    name="⚠️ Aviso",
                    value="Dados de exemplo (MongoDB não disponível)",
                    inline=False,
                )

            embed.set_thumbnail(url=target_user.display_avatar.url)
            embed.set_footer(text="Spy Bot • Sistema de Conquistas")

            await message.channel.send(embed=embed)

        except Exception as e:
            print(f"❌ Erro ao mostrar conquistas: {e}")
            embed = discord.Embed(
                title="❌ Erro",
                description=(
                    "Erro ao buscar conquistas do usuário. "
                    "Tente novamente mais tarde."
                ),
                color=0xFF0000,
                timestamp=datetime.now(),
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(text="Spy Bot • Sistema de Conquistas")
            await message.channel.send(embed=embed)
