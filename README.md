# 🤖 Spy Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-blue.svg)](https://discordpy.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Um bot de Discord para monitoramento de presença, status e salas de voz, com notificações bonitas e estatísticas detalhadas para cada usuário!

---

## ✨ **Funcionalidades**

- **Notificações automáticas** de entrada, saída e mudança de sala de voz (exceto sala excluída)
- **Monitoramento de status** (online, ausente, não incomodar, offline)
- **Estatísticas individuais** com comando `!stats`
- **Mensagens bonitas** usando embeds e emojis
- **Persistência de dados** no MongoDB
- **Configuração fácil** via `.env`

---

## 🚀 **Como instalar**

1. **Clone o repositório:**

   ```bash
   git clone <url-do-repositorio>
   cd spy-bot
   ```

2. **Crie o ambiente virtual:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o arquivo `.env`:**
   - Copie o exemplo:

     ```bash
     cp .env.example .env
     ```

   - Preencha com seu token do bot, ID do canal de notificações e nome da sala a ser ignorada.

---

## ⚙️ **Configuração do `.env`**

```
DISCORD_BOT_TOKEN=seu_token_aqui
CANAL_DE_NOTIFICACAO_ID=1234567890123456789
SALA_EXCLUIDA=VACA WORK OS BRABO
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

- **DISCORD_BOT_TOKEN:** Token do seu bot (obrigatório)
- **CANAL_DE_NOTIFICACAO_ID:** ID do canal onde as notificações serão enviadas (obrigatório)
- **SALA_EXCLUIDA:** Nome da sala de voz que será ignorada pelo monitoramento (opcional)
- **MONGODB_URI:** URI de conexão com o MongoDB (obrigatório)

---

## 🕹️ **Comandos**

- `!stats` — Mostra suas estatísticas de tempo em status e salas de voz

---

## 📦 **Dependências**

- `discord.py`
- `python-dotenv`
- `pymongo`

Instale todas com:

```bash
pip install -r requirements.txt
```

---

## 💡 **Exemplo de uso**

- O bot envia mensagens automáticas e bonitas ao entrar/sair/mudar de sala de voz:
  > ![Exemplo de embed](https://i.imgur.com/2yZbQbA.png)

- Use `!stats` para ver seu tempo online, ausente, em cada sala, etc.:
  > ![Exemplo de stats](https://i.imgur.com/4yQwQwA.png)

---

## 🛡️ **Segurança**

- Nunca compartilhe seu `.env`!
- O arquivo `.env` e dados sensíveis estão no `.gitignore`.

---

## 👨‍💻 **Contribuição**

Pull requests são bem-vindos! Sinta-se à vontade para sugerir melhorias ou reportar bugs.

---

## 🛠️ **Desenvolvimento**

### **Pre-commit Hooks**

O projeto usa pre-commit hooks para garantir qualidade do código:

```bash
# Instalar pre-commit
pip install pre-commit
pre-commit install

# Executar manualmente
pre-commit run --all-files
```

### **Formatação e Linting**

```bash
# Formatar código com Black
black .

# Organizar imports com isort
isort .

# Verificar com flake8
flake8 .
```

### **Versionamento e Releases**

```bash
# Criar novo release (patch, minor, major)
python scripts/release.py patch
python scripts/release.py minor
python scripts/release.py major
```

### **CI/CD**

- ✅ **GitHub Actions** para testes automatizados
- ✅ **Dependabot** para atualizações de dependências
- ✅ **Pre-commit hooks** para qualidade de código
- ✅ **Security scanning** com Bandit

---

## 📄 **Licença**

MIT
