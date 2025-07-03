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
- `!help` — Lista de comandos

### ⚠️ **Alertas e Lembretes**

- **Alertas de inatividade** para membros ausentes
- **Notificações automáticas** de usuários inativos
- **Configuração flexível** de dias para alertas

### 📈 **Relatórios Automáticos**

- **Relatórios semanais** com estatísticas gerais
- **Top usuários** da semana
- **Taxa de atividade** do servidor
- **Conquistas concedidas** no período
- **Agendamento automático** (domingo às 20h)

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
     cp env.example .env
     ```

   - Preencha com seu token do bot, ID do canal de notificações e nome da sala a ser ignorada.

   **⚠️ Importante:** Se você estiver usando `export $(grep -v '^#' .env | xargs)` para carregar as variáveis, certifique-se de que valores com espaços estejam entre aspas no arquivo `.env`:

   ```bash
   # Correto (com aspas)
   REPORT_TIME="sunday 20:00"

   # Incorreto (sem aspas)
   REPORT_TIME=sunday 20:00
   ```

---

## ⚙️ **Configuração do `.env`**

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

- **DISCORD_BOT_TOKEN:** Token do seu bot
- **CANAL_DE_NOTIFICACAO_ID:** ID do canal onde as notificações serão enviadas
- **MONGODB_URI:** URI de conexão com o MongoDB

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
- `!help` — Lista de todos os comandos disponíveis

### **Comandos de Ranking:**

- `!top` — Ranking dos 10 membros com mais tempo online
- `!top voz` — Ranking dos 10 membros com mais tempo em salas de voz

### **Comandos de Conquistas:**

- `!achievements` — Mostra suas conquistas desbloqueadas
- `!achievements @usuario` — Mostra conquistas de outro usuário

### **Comandos de Comparação:**

- `!compare @user1 @user2` — Compara estatísticas de dois usuários

### **Comandos de Servidor:**

- `!serverstats` — Estatísticas gerais do servidor

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
