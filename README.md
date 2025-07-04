# 🤖 Spy Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-blue.svg)](https://discordpy.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Make](https://img.shields.io/badge/Makefile-Available-green.svg)](https://www.gnu.org/software/make/)
[![wakatime](https://wakatime.com/badge/user/47ec2352-4b0b-4d3c-b270-5649937dd18b/project/c157a9c7-b539-4c0a-895b-1518dbbc2795.svg)](https://wakatime.com/badge/user/47ec2352-4b0b-4d3c-b270-5649937dd18b/project/c157a9c7-b539-4c0a-895b-1518dbbc2795)

A Discord bot for monitoring presence, status, and voice channels with beautiful notifications and detailed statistics for each user!

---

## 🌍 **Languages**

- 🇺🇸 [English](README.md)
- 🇧🇷 [Português](README-pt-br.md)

---

## ✨ **Features**

### 🎯 **Basic Monitoring**

- **Automatic notifications** for joining, leaving, and changing voice channels (except excluded channel)
- **Status monitoring** (online, idle, do not disturb, offline)
- **Platform detection** (Mobile/Desktop) for joins and leaves
- **Beautiful messages** using embeds and emojis
- **Data persistence** in MongoDB

### 🏆 **Rankings and Achievements System**

- **Automatic achievements** based on online time, voice activity, and engagement
- **Competitive rankings** of the most active members
- **Achievement notifications** when unlocked
- **Medals and badges** for different types of activity

### 📊 **Advanced Commands**

- `!stats` — Detailed personal statistics
- `!top` — Ranking of the 10 most active members
- `!top voice` — Ranking of those who used voice the most
- `!achievements` — Your achievements
- `!compare @user1 @user2` — Compare users
- `!serverstats` — General server statistics
- `!clear` — Clear all messages from the current channel (requires permission)
- `!silence` — Shows a tutorial on how to mute the channel manually in Discord (via DM)
- `!help` — List of commands

### ⚠️ **Alerts and Reminders**

- **Inactivity alerts** for absent members
- **Automatic notifications** for inactive users
- **Flexible configuration** of days for alerts

### 🔇 **Silence System**

- **User-controlled notifications** - Users can silence bot notifications
- **Flexible duration** - Temporary (hours/days) or permanent silence
- **Automatic expiration** - Temporary silences expire automatically
- **Permission-based access** - Requires "Manage Messages" permission

### 📈 **Automatic Reports**

- **Weekly reports** with general statistics
- **Top users** of the week
- **Server activity rate**
- **Achievements granted** in the period
- **Automatic scheduling** (Sunday at 8 PM)

### 💤 **Sleep Mode**

- `!sleep` — Puts the bot to sleep until it receives `!wake`.
- `!sleep 30m` / `!sleep 2h` / `!sleep 1d` — Bot sleeps for the specified time (minutes, hours, days).
- `!wake` — Wakes the bot up immediately.
- `!status-sleep` — Shows the current sleep mode status.

**While sleeping:**

- The bot **continues collecting all metrics normally** (presence, voice, messages, achievements, etc).
- The bot **does not send automatic messages** (reports, alerts, unlocked achievements, etc).
- The bot **still responds to commands**.

### **Silence Commands:**

- `!silence` — Shows a tutorial on how to mute the channel manually in Discord (via DM).

> The !silence command only teaches you how to mute the channel manually. The bot cannot mute channels for you, as this is a personal Discord setting.

### **Ranking Commands:**

- `!top` — Ranking of the 10 members with the most online time
- `!top voice` — Ranking of the 10 members with the most time in voice channels

### **Achievement Commands:**

- `!achievements` — Shows your unlocked achievements
- `!achievements @user` — Shows achievements of another user
- `!achievements-categories` — Shows all achievement categories and how many there are in each (dare to collect them all!)

#### **Achievement Categories (Examples):**

- 🎤 Voice & Presence — For the most sociable! (e.g., stay 24h in voice?)
- 💬 Messages & Reactions — For the most active! (1000 messages in a day?)
- 🦋 Social & Community — For the most popular! (help 50 people?)
- 📈 Engagement & Usage — For the most dedicated! (7 days online without a break?)
- ⏰ Activity & Consistency — For the most persistent! (30 days in a row?)
- 🎲 Fun & Extras — For the most creative! (use all custom emojis?)
- 🌙 Discord Lunatic — For the craziest! (online at dawn?)

*Unlock all 50 achievements and become a Discord legend! Less than 1% can do it... Will you?*

### **Comparison Commands:**

- `!compare @user1 @user2` — Compares statistics of two users

### **Server Commands:**

- `!serverstats` — General server statistics

### **Silence System Examples:**

**Temporary Silence:**

- `!silence_2h` — Silence notifications for 2 hours
- `!silence_1d` — Silence notifications for 1 day
- `!silence_7d` — Silence notifications for 1 week

**Permanent Silence:**

- `!silence_always` — Permanently silence all bot notifications

### **Management:**

- `!silence_status` — Check current silence status
- `!silence_remove` — Remove silence and resume notifications

---

## 🚀 **Installation**

### **Option 1: Docker (Recommended)**

The easiest way to run Spy Bot is using Docker Compose, which includes MongoDB:

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd spy-bot
   ```

2. **Configure the `.env` file:**
   - Copy the example:

     ```bash
     cp env.example .env
     ```

   - Fill in with your bot token, notification channel ID, and MongoDB credentials.

3. **Run with Docker Compose:**

   ```bash
   docker-compose up -d
   ```

   This will start both the bot and MongoDB automatically.

### **Option 2: Manual Installation**

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd spy-bot
   ```

2. **Create the virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the `.env` file:**
   - Copy the example:

     ```bash
     cp env.example .env
     ```

   - Fill in with your bot token, notification channel ID, and MongoDB connection string.

   **⚠️ Important:** If you're using `export $(grep -v '^#' .env | xargs)` to load variables, make sure values with spaces are in quotes in the `.env` file:

   ```bash
   # Correct (with quotes)
   REPORT_TIME="sunday 20:00"

   # Incorrect (without quotes)
   REPORT_TIME=sunday 20:00
   ```

5. **Run the bot:**

   ```bash
   python main.py
   ```

---

## ⚙️ **`.env` Configuration**

### **For Docker Installation:**

```
# Required Settings
DISCORD_BOT_TOKEN=your_token_here
CANAL_DE_NOTIFICACAO_ID=1234567890123456789

# MongoDB Settings (for Docker)
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password123
MONGO_INITDB_DATABASE=spy
MONGODB_URI=mongodb://admin:password123@alert-mongo:27017/spy?authSource=admin

# Optional Settings
SALA_EXCLUIDA=VACA WORK OS BRABO
CANAL_RELATORIOS_ID=1234567890123456789
CANAL_ALERTAS_ID=1234567890123456789
REPORT_TIME=sunday 20:00
ALERT_INACTIVE_DAYS=7
```

### **For Manual Installation:**

```
# Required Settings
DISCORD_BOT_TOKEN=your_token_here
CANAL_DE_NOTIFICACAO_ID=1234567890123456789
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority

# Optional Settings
SALA_EXCLUIDA=VACA WORK OS BRABO
CANAL_RELATORIOS_ID=1234567890123456789
CANAL_ALERTAS_ID=1234567890123456789
REPORT_TIME=sunday 20:00
ALERT_INACTIVE_DAYS=7
```

### **Required Settings:**

- **DISCORD_BOT_TOKEN:** Your bot token from Discord Developer Portal
- **CANAL_DE_NOTIFICACAO_ID:** ID of the channel where notifications will be sent
- **MONGODB_URI:** MongoDB connection URI (for manual installation)

### **Docker-specific Settings:**

- **MONGO_INITDB_ROOT_USERNAME:** MongoDB root username (for Docker)
- **MONGO_INITDB_ROOT_PASSWORD:** MongoDB root password (for Docker)
- **MONGO_INITDB_DATABASE:** MongoDB database name (for Docker)

### **Optional Settings:**

- **SALA_EXCLUIDA:** Name of the voice channel that will be ignored by monitoring
- **CANAL_RELATORIOS_ID:** ID of the channel where weekly reports will be sent
- **CANAL_ALERTAS_ID:** ID of the channel where inactivity alerts will be sent
- **REPORT_TIME:** Time for sending the weekly report (default: "sunday 20:00")
- **ALERT_INACTIVE_DAYS:** Number of days to consider a user inactive (default: 7)

---

## 🕹️ **Commands**

### **Basic Commands:**

- `!stats` — Shows your statistics of time in status and voice channels
- `!clear` — Clear all messages from the current channel (requires "Manage Messages" permission)
- `!help` — List of all available commands

### **Silence Commands:**

- `!silence` — Shows a tutorial on how to mute the channel manually in Discord (via DM).

> The !silence command only teaches you how to mute the channel manually. The bot cannot mute channels for you, as this is a personal Discord setting.

### **Ranking Commands:**

- `!top` — Ranking of the 10 members with the most online time
- `!top voice` — Ranking of the 10 members with the most time in voice channels

### **Achievement Commands:**

- `!achievements` — Shows your unlocked achievements
- `!achievements @user` — Shows achievements of another user
- `!achievements-categories` — Shows all achievement categories and how many there are in each (dare to collect them all!)

#### **Achievement Categories (Examples):**

- 🎤 Voice & Presence — For the most sociable! (e.g., stay 24h in voice?)
- 💬 Messages & Reactions — For the most active! (1000 messages in a day?)
- 🦋 Social & Community — For the most popular! (help 50 people?)
- 📈 Engagement & Usage — For the most dedicated! (7 days online without a break?)
- ⏰ Activity & Consistency — For the most persistent! (30 days in a row?)
- 🎲 Fun & Extras — For the most creative! (use all custom emojis?)
- 🌙 Discord Lunatic — For the craziest! (online at dawn?)

*Unlock all 50 achievements and become a Discord legend! Less than 1% can do it... Will you?*

### **Comparison Commands:**

- `!compare @user1 @user2` — Compares statistics of two users

### **Server Commands:**

- `!serverstats` — General server statistics

### **Silence System Examples:**

**Temporary Silence:**

- `!silence_2h` — Silence notifications for 2 hours
- `!silence_1d` — Silence notifications for 1 day
- `!silence_7d` — Silence notifications for 1 week

**Permanent Silence:**

- `!silence_always` — Permanently silence all bot notifications

### **Management:**

- `!silence_status` — Check current silence status
- `!silence_remove` — Remove silence and resume notifications

## 📦 **Dependencies**

### **Core Dependencies:**

- `discord.py>=2.0.0` - Discord API wrapper
- `python-dotenv>=0.19.0` - Environment variable management
- `pymongo>=4.0.0` - MongoDB driver

### **Development Dependencies:**

- `black>=23.0.0` - Code formatter
- `flake8>=6.0.0` - Linter
- `isort>=5.12.0` - Import sorter
- `bandit>=1.7.5` - Security linter
- `pre-commit>=3.0.0` - Git hooks

### **Installation:**

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies
pip install -e .[dev]
```

---

## 💡 **Usage Example**

### **Automatic Notifications:**

- The bot sends automatic and beautiful messages when joining/leaving/changing voice channels:
  > ![Embed example](https://i.imgur.com/2yZbQbA.png)

### **Personal Statistics:**

- Use `!stats` to see your online time, idle time, time in each channel, etc.:
  > ![Stats example](https://i.imgur.com/4yQwQwA.png)

### **Achievement System:**

- **⏰ First Hour** — Stayed online for 1 hour
- **🔥 Dedicated** — Stayed online for 10 hours
- **👑 Veteran** — Stayed online for 50 hours
- **🎤 Voice Explorer** — Spent 1 hour in voice channels
- **🎵 Voice Master** — Spent 10 hours in voice channels
- **🦋 Social Butterfly** — Visited 3 different channels
- **🏠 Channel Explorer** — Visited 10 different channels

### **Weekly Reports:**

- Automatically sent every Sunday at 8 PM
- Include top users, general statistics, and weekly achievements

---

## 🛡️ **Security**

- Never share your `.env`!
- The `.env` file and sensitive data are in `.gitignore`.

---

## 🔧 **Troubleshooting**

### **Environment variables problem:**

If you get the error `export: not an identifier` when loading `.env`, it's because some variable contains spaces. Solutions:

1. **Use quotes in the `.env` file:**

   ```bash
   REPORT_TIME="sunday 20:00"
   ```

2. **Or use python-dotenv (recommended):**

   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

3. **Or load manually:**

   ```bash
   source .env
   ```

### **Bot doesn't respond to commands:**

- Check if the bot has permission to read messages
- Confirm that `MESSAGE_CONTENT_INTENT` is enabled in the Discord Developer Portal

### **Reports are not sent:**

- Check if `CANAL_RELATORIOS_ID` is configured correctly
- Confirm that the bot has permission to send messages in the channel

### **Docker issues:**

- **MongoDB connection failure:** Check if the MongoDB container is running with `docker-compose ps`
- **Bot doesn't start:** Check logs with `docker-compose logs alert-bot`
- **Environment variables not loaded:** Make sure the `.env` file exists and has correct format
- **Port conflicts:** Change MongoDB port in `docker-compose.yml` if 27843 is already in use

---

## 📄 **License**

- [MIT](./LICENSE)
