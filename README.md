# 🤖 Spy Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-blue.svg)](https://discordpy.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

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
- `!help` — List of commands

### ⚠️ **Alerts and Reminders**

- **Inactivity alerts** for absent members
- **Automatic notifications** for inactive users
- **Flexible configuration** of days for alerts

### 📈 **Automatic Reports**

- **Weekly reports** with general statistics
- **Top users** of the week
- **Server activity rate**
- **Achievements granted** in the period
- **Automatic scheduling** (Sunday at 8 PM)

---

## 🚀 **How to install**

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

   - Fill in with your bot token, notification channel ID, and name of the channel to be ignored.

   **⚠️ Important:** If you're using `export $(grep -v '^#' .env | xargs)` to load variables, make sure values with spaces are in quotes in the `.env` file:

   ```bash
   # Correct (with quotes)
   REPORT_TIME="sunday 20:00"

   # Incorrect (without quotes)
   REPORT_TIME=sunday 20:00
   ```

---

## ⚙️ **`.env` Configuration**

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

- **DISCORD_BOT_TOKEN:** Your bot token
- **CANAL_DE_NOTIFICACAO_ID:** ID of the channel where notifications will be sent
- **MONGODB_URI:** MongoDB connection URI

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
- `!help` — List of all available commands

### **Ranking Commands:**

- `!top` — Ranking of the 10 members with the most online time
- `!top voice` — Ranking of the 10 members with the most time in voice channels

### **Achievement Commands:**

- `!achievements` — Shows your unlocked achievements
- `!achievements @user` — Shows achievements of another user

### **Comparison Commands:**

- `!compare @user1 @user2` — Compares statistics of two users

### **Server Commands:**

- `!serverstats` — General server statistics

---

## 📦 **Dependencies**

- `discord.py`
- `python-dotenv`
- `pymongo`

Install all with:

```bash
pip install -r requirements.txt
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

---

## 👨‍💻 **Contribution**

Pull requests are welcome! Feel free to suggest improvements or report bugs.

---

## 🛠️ **Development**

### **Pre-commit Hooks**

The project uses pre-commit hooks to ensure code quality:

```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

### **Formatting and Linting**

```bash
# Format code with Black
black .

# Organize imports with isort
isort .

# Check with flake8
flake8 .
```

### **Versioning and Releases**

```bash
# Create new release (patch, minor, major)
python scripts/release.py patch
python scripts/release.py minor
python scripts/release.py major
```

### **CI/CD**

- ✅ **GitHub Actions** for automated testing
- ✅ **Dependabot** for dependency updates
- ✅ **Pre-commit hooks** for code quality
- ✅ **Security scanning** with Bandit

---

## �� **License**

MIT
