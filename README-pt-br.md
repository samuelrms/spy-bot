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

Um bot de Discord para monitoramento de presença, status e salas de voz, com notificações bonitas e estatísticas detalhadas para cada usuário!

---

## 🌍 **Idiomas**

- 🇺🇸 [English](README.md)
- 🇧🇷 [Português](README-pt-br.md)

## ✨ **Funcionalidades**

### 🎯 **Monitoramento Básico**

- **Notificações automáticas** de entrada, saída e mudança de sala de voz (exceto sala excluída)
- **Monitoramento de status** (online, ausente, não incomodar, offline)
- **Detecção de plataforma** (Mobile/Desktop) nas entradas e saídas
- **Mensagens bonitas** usando embeds e emojis
- **Persistência de dados** no MongoDB

### 🏆 **Sistema de Rankings e Conquistas**

- **Conquistas automáticas** baseadas em tempo online, voz e atividade
- **Rankings competitivos** dos membros mais ativos
- **Notificações de conquistas** quando desbloqueadas
- **Medalhas e badges** por diferentes tipos de atividade

### 📊 **Comandos Avançados**

- `!stats` — Estatísticas pessoais detalhadas
- `!top` — Ranking dos 10 mais ativos
- `!top voz` — Ranking dos que mais usaram voz
- `!achievements` — Suas conquistas
- `!compare @user1 @user2` — Comparar usuários
- `!serverstats` — Estatísticas gerais do servidor
- `!clear` — Limpa todas as mensagens do canal atual (requer permissão)
- `!silence` — Mostra um tutorial de como silenciar o canal manualmente pelo Discord (via DM)
- `!help` — Lista de comandos

### ⚠️ **Alertas e Lembretes**

- **Alertas de inatividade** para membros ausentes
- **Notificações automáticas** de usuários inativos
- **Configuração flexível** de dias para alertas

### 🔇 **Sistema de Silenciamento**

- **Controle de notificações** - Usuários podem silenciar notificações do bot
- **Duração flexível** - Silenciamento temporário (horas/dias) ou permanente
- **Expiração automática** - Silenciamentos temporários expiram automaticamente
- **Acesso baseado em permissões** - Requer permissão "Gerenciar Mensagens"

### 📈 **Relatórios Automáticos**

- **Relatórios semanais** com estatísticas gerais
- **Top usuários** da semana
- **Taxa de atividade** do servidor
- **Conquistas concedidas** no período
- **Agendamento automático** (domingo às 20h)

### 💤 **Modo Sleep (Silencioso)**

- `!sleep` — Coloca o bot para dormir até receber `!wake`.
- `!sleep 30m` / `!sleep 2h` / `!sleep 1d` — Bot dorme pelo tempo especificado (minutos, horas, dias).
- `!wake` — Acorda o bot imediatamente.
- `!status-sleep` — Mostra o status atual do modo sleep.

**Enquanto dormindo:**

- O bot **continua coletando todas as métricas normalmente** (presença, voz, mensagens, conquistas, etc).
- O bot **não envia mensagens automáticas** (relatórios, alertas, conquistas desbloqueadas, etc).
- O bot **responde normalmente aos comandos**.

---

## 🚀 **Instalação**

### **Opção 1: Docker (Recomendado)**

A forma mais fácil de executar o Spy Bot é usando Docker Compose, que inclui MongoDB:

1. **Clone o repositório:**

   ```bash
   git clone <url-do-repositorio>
   cd spy-bot
   ```

2. **Configure o arquivo `.env`:**
   - Copie o exemplo:

     ```bash
     cp env.example .env
     ```

   - Preencha com seu token do bot, ID do canal de notificações e credenciais do MongoDB.

3. **Execute com Docker Compose:**

   ```bash
   docker-compose up -d
   ```

   Isso iniciará tanto o bot quanto o MongoDB automaticamente.

### **Opção 2: Instalação Manual**

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
     cp env.example .env
     ```

   - Preencha com seu token do bot, ID do canal de notificações e string de conexão do MongoDB.

   **⚠️ Importante:** Se você estiver usando `export $(grep -v '^#' .env | xargs)` para carregar as variáveis, certifique-se de que valores com espaços estejam entre aspas no arquivo `.env`:

   ```bash
   # Correto (com aspas)
   REPORT_TIME="sunday 20:00"

   # Incorreto (sem aspas)
   REPORT_TIME=sunday 20:00
   ```

5. **Execute o bot:**

   ```bash
   python main.py
   ```

---

## ⚙️ **Configuração do `.env`**

### **Para Instalação com Docker:**

```
# Configurações Obrigatórias
DISCORD_BOT_TOKEN=seu_token_aqui
CANAL_DE_NOTIFICACAO_ID=1234567890123456789

# Configurações do MongoDB (para Docker)
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password123
MONGO_INITDB_DATABASE=spy
MONGODB_URI=mongodb://admin:password123@alert-mongo:27017/spy?authSource=admin

# Configurações Opcionais
SALA_EXCLUIDA=VACA WORK OS BRABO
CANAL_RELATORIOS_ID=1234567890123456789
CANAL_ALERTAS_ID=1234567890123456789
REPORT_TIME=sunday 20:00
ALERT_INACTIVE_DAYS=7
```

### **Para Instalação Manual:**

```
# Configurações Obrigatórias
DISCORD_BOT_TOKEN=seu_token_aqui
CANAL_DE_NOTIFICACAO_ID=1234567890123456789
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority

# Configurações Opcionais
SALA_EXCLUIDA=VACA WORK OS BRABO
CANAL_RELATORIOS_ID=1234567890123456789
CANAL_ALERTAS_ID=1234567890123456789
REPORT_TIME=sunday 20:00
ALERT_INACTIVE_DAYS=7
```

### **Configurações Obrigatórias:**

- **DISCORD_BOT_TOKEN:** Token do seu bot do Discord Developer Portal
- **CANAL_DE_NOTIFICACAO_ID:** ID do canal onde as notificações serão enviadas
- **MONGODB_URI:** URI de conexão com o MongoDB (para instalação manual)

### **Configurações Específicas do Docker:**

- **MONGO_INITDB_ROOT_USERNAME:** Nome de usuário root do MongoDB (para Docker)
- **MONGO_INITDB_ROOT_PASSWORD:** Senha root do MongoDB (para Docker)
- **MONGO_INITDB_DATABASE:** Nome do banco de dados MongoDB (para Docker)

### **Configurações Opcionais:**

- **SALA_EXCLUIDA:** Nome da sala de voz que será ignorada pelo monitoramento
- **CANAL_RELATORIOS_ID:** ID do canal onde os relatórios semanais serão enviados
- **CANAL_ALERTAS_ID:** ID do canal onde os alertas de inatividade serão enviados
- **REPORT_TIME:** Horário para envio do relatório semanal (padrão: "sunday 20:00")
- **ALERT_INACTIVE_DAYS:** Número de dias para considerar um usuário inativo (padrão: 7)

---

## 🕹️ **Comandos**

### **Comandos Básicos:**

- `!stats` — Mostra suas estatísticas de tempo em status e salas de voz
- `!clear` — Limpa todas as mensagens do canal atual (requer permissão "Gerenciar Mensagens")
- `!help` — Lista de todos os comandos disponíveis

---

## 📦 **Dependências**

### **Dependências Principais:**

- `discord.py>=2.0.0` - Wrapper da API do Discord
- `python-dotenv>=0.19.0` - Gerenciamento de variáveis de ambiente
- `pymongo>=4.0.0` - Driver do MongoDB

### **Dependências de Desenvolvimento:**

- `black>=23.0.0` - Formatador de código
- `flake8>=6.0.0` - Linter
- `isort>=5.12.0` - Organizador de imports
- `bandit>=1.7.5` - Linter de segurança
- `pre-commit>=3.0.0` - Git hooks

### **Instalação:**

```bash
# Dependências de produção
pip install -r requirements.txt

# Dependências de desenvolvimento
pip install -e .[dev]
```

---

## 💡 **Exemplo de uso**

### **Notificações Automáticas:**

- O bot envia mensagens automáticas e bonitas ao entrar/sair/mudar de sala de voz:
  > ![Exemplo de embed](https://i.imgur.com/2yZbQbA.png)

### **Estatísticas Pessoais:**

- Use `!stats` para ver seu tempo online, ausente, em cada sala, etc.:
  > ![Exemplo de stats](https://i.imgur.com/4yQwQwA.png)

### **Sistema de Conquistas:**

- **⏰ Primeira Hora** — Ficou online por 1 hora
- **🔥 Dedicado** — Ficou online por 10 horas
- **👑 Veterano** — Ficou online por 50 horas
- **🎤 Explorador de Voz** — Passou 1 hora em salas de voz
- **🎵 Mestre da Voz** — Passou 10 horas em salas de voz
- **🦋 Borboleta Social** — Visitou 3 salas diferentes
- **🏠 Explorador de Salas** — Visitou 10 salas diferentes

### **Relatórios Semanais:**

- Enviados automaticamente todo domingo às 20h
- Incluem top usuários, estatísticas gerais e conquistas da semana

---

## 🛡️ **Segurança**

- Nunca compartilhe seu `.env`!
- O arquivo `.env` e dados sensíveis estão no `.gitignore`.

---

## 🔧 **Troubleshooting**

### **Problema com variáveis de ambiente:**

Se você receber erro `export: not an identifier` ao carregar o `.env`, é porque alguma variável contém espaços. Soluções:

1. **Use aspas no arquivo `.env`:**

   ```bash
   REPORT_TIME="sunday 20:00"
   ```

2. **Ou use o python-dotenv (recomendado):**

   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

3. **Ou carregue manualmente:**

   ```bash
   source .env
   ```

### **Bot não responde aos comandos:**

- Verifique se o bot tem permissão para ler mensagens
- Confirme se o `MESSAGE_CONTENT_INTENT` está habilitado no Discord Developer Portal

### **Relatórios não são enviados:**

- Verifique se `CANAL_RELATORIOS_ID` está configurado corretamente
- Confirme se o bot tem permissão para enviar mensagens no canal

### **Problemas com Docker:**

- **Falha na conexão com MongoDB:** Verifique se o container MongoDB está rodando com `docker-compose ps`
- **Bot não inicia:** Verifique os logs com `docker-compose logs alert-bot`
- **Variáveis de ambiente não carregadas:** Certifique-se de que o arquivo `.env` existe e tem formato correto
- **Conflitos de porta:** Altere a porta do MongoDB no `docker-compose.yml` se 27843 já estiver em uso

---

## 👨‍💻 **Contribuição**

Pull requests são bem-vindos! Sinta-se à vontade para sugerir melhorias ou reportar bugs.

---

## 🛠️ **Desenvolvimento**

### **Início Rápido com Makefile**

O projeto inclui um Makefile para tarefas comuns de desenvolvimento:

```bash
# Mostrar todos os comandos disponíveis
make help

# Configuração inicial para desenvolvimento
make setup

# Executar todas as verificações (format, lint, test)
make check

# Formatar código
make format

# Executar linting
make lint

# Executar pre-commit hooks
make pre-commit
```

### **Comandos Manuais de Desenvolvimento**

```bash
# Formatar código com Black
black .

# Organizar imports com isort
isort .

# Verificar com flake8
flake8 .

# Verificação de segurança com Bandit
bandit -r . -f json -o bandit-report.json

# Criar novo release
python scripts/release.py patch
```

### **CI/CD**

- ✅ **GitHub Actions** para testes automatizados
- ✅ **Dependabot** para atualizações de dependências
- ✅ **Pre-commit hooks** para qualidade de código
- ✅ **Security scanning** com Bandit
- ✅ **Suporte a Docker** para deploy fácil

---

## 📄 **Licença**

- [MIT](./LICENSE)

## 📄 **Licença**

- [MIT](./LICENSE)
