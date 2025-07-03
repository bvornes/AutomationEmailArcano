# 🔮 Automação de Emails - Quiz Arcanos

Automação para envio de emails personalizados para recuperação de leads do quiz de arcanos.

## 🚀 Deploy no Render.com

Este projeto está configurado para deploy automático no Render.com como um Cron Job.

### 📋 Arquivos do Projeto

- `main.py` - Script principal da automação
- `requirements.txt` - Dependências Python
- `render.yaml` - Configuração do Render.com
- `convert_json.py` - Utilitário para converter credentials.json

### ⚙️ Configuração

1. **Variáveis de Ambiente no Render:**
   - `SHEET_URL` - URL da planilha Google Sheets
   - `WORKSHEET_NAME` - Nome da aba (Página1)
   - `EMAIL_SENDER` - Email remetente (madame.celeste7@gmail.com)
   - `EMAIL_NAME` - Nome do remetente (Madame Celeste)
   - `EMAIL_PASS` - Senha de aplicativo do Gmail
   - `GOOGLE_CREDENTIALS_JSON` - Credenciais da Service Account (JSON em linha única)

2. **Schedule Configurado:**
   - Executa a cada 6 horas: `0 */6 * * *`

### 🔮 Templates de Arcanos

- The Hierophant
- The Hermit
- Death
- The Magician
- Temperance
- Strength

### 📊 Funcionamento

1. Conecta com Google Sheets via Service Account
2. Lê registros com `Email_Enviado = FALSE`
3. Envia email personalizado baseado no arcano
4. Marca como `TRUE` na planilha
5. Registra data/hora do envio

### 🛡️ Segurança

- Credenciais armazenadas em variáveis de ambiente
- Arquivo credentials.json não incluído no repositório
- Delay entre envios para evitar spam

---

**🎯 Objetivo:** Recuperar leads que abandonaram o quiz de arcanos com emails personalizados e místicos.