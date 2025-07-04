import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CANAL_DE_NOTIFICACAO_ID = int(os.getenv("CANAL_DE_NOTIFICACAO_ID"))
SALA_EXCLUIDA = os.getenv("SALA_EXCLUIDA")

CANAL_RELATORIOS_ID = int(os.getenv("CANAL_RELATORIOS_ID")) or None
CANAL_ALERTAS_ID = int(os.getenv("CANAL_ALERTAS_ID")) or None
REPORT_TIME = os.getenv("REPORT_TIME", "sunday 20:00")
ALERT_INACTIVE_DAYS = int(os.getenv("ALERT_INACTIVE_DAYS"))

MONGODB_URI = os.getenv("MONGODB_URI")

DISCORD_INTENTS = {
    "guilds": True,
    "members": True,
    "presences": True,
    "voice_states": True,
    "message_content": True,
    "reactions": True,
}

ACHIEVEMENT_CATEGORIES = [
    "🎤 Voz & Presença",
    "💬 Mensagens & Reações",
    "🦋 Social & Comunidade",
    "📈 Engajamento & Uso",
    "⏰ Atividade & Consistência",
    "🎲 Diversão & Extras",
    "🌙 Lunático do Discord",
]

WELCOME_KEYWORDS = [
    "bem-vindo",
    "bem vindo",
    "welcome",
    "bem-vinda",
    "bem vinda",
    "seja bem-vindo",
    "seja bem vindo",
]
HELP_KEYWORDS = [
    "ajuda",
    "help",
    "como",
    "dúvida",
    "duvida",
    "problema",
    "solução",
    "resposta",
]
PEACE_KEYWORDS = [
    "calma",
    "paz",
    "tranquilo",
    "respeito",
    "vamos conversar",
    "sem brigas",
    "sem discussão",
]
POLL_KEYWORDS = [
    "enquete",
    "poll",
    "votação",
    "votacao",
    "votem",
    "vote",
    "opinião",
    "opiniao",
]
HEART_EMOJIS = ["❤️", "💖", "💕", "💗", "💓", "💝", "💘", "💞"]
