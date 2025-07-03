import gspread
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import time
import json

# ===== CONFIGURAÇÕES VIA VARIÁVEIS DE AMBIENTE =====
SHEET_URL = os.getenv('SHEET_URL', 'https://docs.google.com/spreadsheets/d/1VHcC3CKnBBJKjTap_IsGJSku9clD0mjGsHnwc71h5iI/edit#gid=0')
WORKSHEET_NAME = os.getenv('WORKSHEET_NAME', 'Página1')

# Gmail configuration
EMAIL_SENDER = os.getenv('EMAIL_SENDER', 'madame.celeste7@gmail.com')
EMAIL_PASS = os.getenv('EMAIL_PASS', 'wdaj lhhr xuvb flog')
EMAIL_NAME = os.getenv('EMAIL_NAME', 'Madame Celeste')

# Google Credentials from environment variable (JSON string)
GOOGLE_CREDENTIALS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON')

# ===== TEMPLATES DE EMAIL POR ARCANO =====
arcano_templates = {
    "The Hierophant": {
        "subject": "🔮 You carry the ancient wisdom — Arcana of the Hierophant",
        "body": lambda name, link: f"""Hello {name},

Your soul is touched by the Hierophant.
You were born with divine insight — but your sacred path is incomplete.

There are 3 divine truths you've yet to uncover.
⏳ Time is limited.

Click below to complete your Arcana revelation:
{link}

May the stars guide you,
Madame Celeste""",
        "link": "https://pay.hotmart.com/L100591285J"
    },
    "The Hermit": {
        "subject": "🌟 Your path is not lonely — The Hermit has a message for you",
        "body": lambda name, link: f"""Hi {name},

The Arcana of the Hermit surrounds you.
You are the seeker — walking paths others fear.

But your answers lie beyond what you've seen.
3 powerful truths await your discovery.

✨ Open the hidden message now:
{link}

Blessings on your journey,
Madame Celeste""",
        "link": "https://pay.hotmart.com/N100591815W"
    },
    "Death": {
        "subject": "🔥 Your rebirth is waiting — don't miss it",
        "body": lambda name, link: f"""Hello {name},

I felt your energy echoing through the veil…
You carry the Arcana of Death, a symbol of deep transformation.

You began the journey… but stopped at the gates.
And yet, 3 sacred truths are still waiting to be revealed.

⏳ The portal is closing fast.
You must act now — or risk missing your cosmic awakening.

✨ Click here to unlock what still lies hidden:
{link}

In cosmic light,
Madame Celeste""",
        "link": "https://pay.hotmart.com/H100591429B"
    },
    "The Magician": {
        "subject": "⚡ You carry the Arcana of the Magician — your power is awakening",
        "body": lambda name, link: f"""Hello {name},

Your energy echoes with creation and manifestation.
You carry the Arcana of the Magician — the one who transforms intention into reality.

But your ritual is not complete yet.
3 hidden secrets remain to be revealed.

🌕 The portal closes soon.
Click here to complete your Arcana reading:
{link}

Channel your power,
Madame Celeste""",
        "link": "https://pay.hotmart.com/L100590752Q"
    },
    "Temperance": {
        "subject": "⚖️ Balance is your gift — The Arcana of Temperance has spoken",
        "body": lambda name, link: f"""Dear {name},

The divine balance flows through your spirit.
You were chosen by the Arcana of Temperance — a rare harmony in a world of chaos.

Yet the full message still sleeps.
You must awaken it before time runs out.

🔮 Click now to reveal the remaining 3 secrets:
{link}

In divine balance,
Madame Celeste""",
        "link": "https://pay.hotmart.com/T100598874Q"
    },
    "Strength": {
        "subject": "💪 You bear the Strength — but 3 sacred forces remain hidden",
        "body": lambda name, link: f"""Hi {name},

The Arcana of Strength flows through your being.
You've survived storms others couldn't.

But your destiny hasn't fully awakened.
Three powers still slumber in your soul.

💫 Don't let them stay hidden.
Unlock your full revelation here:
{link}

With inner strength,
Madame Celeste""",
        "link": "https://pay.hotmart.com/R100591709I"
    }
}

def conectar_planilha():
    """Conecta com o Google Sheets usando service account"""
    try:
        if not GOOGLE_CREDENTIALS_JSON:
            print("❌ GOOGLE_CREDENTIALS_JSON não configurado!")
            return None
            
        # Parse JSON credentials from environment variable
        credentials_info = json.loads(GOOGLE_CREDENTIALS_JSON)
        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(credentials_info, scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(SHEET_URL).worksheet(WORKSHEET_NAME)
        print("✅ Google Sheets conectado com sucesso!")
        return sheet
    except Exception as e:
        print(f"❌ Erro ao conectar Google Sheets: {e}")
        return None

def conectar_gmail():
    """Conecta com o servidor SMTP do Gmail"""
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASS)
        print("✅ Gmail conectado com sucesso!")
        return server
    except Exception as e:
        print(f"❌ Erro ao conectar Gmail: {e}")
        return None

def enviar_email(server, destinatario, nome, arcano):
    """Envia email personalizado baseado no arcano"""
    if arcano not in arcano_templates:
        print(f"⚠️  Template não encontrado para arcano: '{arcano}'")
        return False
    
    template = arcano_templates[arcano]
    
    try:
        msg = MIMEMultipart()
        msg["From"] = f"{EMAIL_NAME} <{EMAIL_SENDER}>"
        msg["To"] = destinatario
        msg["Subject"] = template["subject"]
        
        corpo = template["body"](nome, template["link"])
        msg.attach(MIMEText(corpo, "plain", "utf-8"))
        
        server.sendmail(EMAIL_SENDER, [destinatario], msg.as_string())
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar email para {destinatario}: {e}")
        return False

def main():
    """Função principal da automação"""
    print("=" * 60)
    print("🔮 AUTOMAÇÃO DE EMAILS - ARCANOS QUIZ (RENDER)")
    print("=" * 60)
    print(f"⏰ Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Conectar com planilha
    sheet = conectar_planilha()
    if not sheet:
        return
    
    # Conectar com Gmail
    server = conectar_gmail()
    if not server:
        return
    
    # Ler dados da planilha
    try:
        print("📊 Lendo dados da planilha...")
        data = sheet.get_all_records()
        print(f"📋 Total de registros: {len(data)}")
        
        pendentes = [row for row in data if str(row.get("Email_Enviado", "")).upper() == "FALSE"]
        print(f"📧 Emails pendentes: {len(pendentes)}")
        
        if len(pendentes) == 0:
            print("✅ Nenhum email pendente para envio!")
            server.quit()
            return
            
    except Exception as e:
        print(f"❌ Erro ao ler planilha: {e}")
        server.quit()
        return
    
    # Processar envios
    print("\n🚀 INICIANDO ENVIOS")
    emails_enviados = 0
    emails_com_erro = 0
    
    for idx, row in enumerate(data, start=2):
        if str(row.get("Email_Enviado", "")).upper() == "FALSE":
            nome = row.get("Nome", "").strip()
            email = row.get("Email", "").strip()
            arcano = row.get("Nome_Arcano", "").strip()
            
            if not nome or not email or not arcano:
                print(f"⚠️  Linha {idx}: Dados incompletos")
                emails_com_erro += 1
                continue
            
            print(f"📧 Enviando para: {nome} ({email}) - {arcano}")
            
            if enviar_email(server, email, nome, arcano):
                try:
                    sheet.update_cell(idx, 9, "TRUE")
                    sheet.update_cell(idx, 10, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    emails_enviados += 1
                    print(f"✅ Email enviado!")
                    time.sleep(2)  # Delay entre envios
                except Exception as e:
                    print(f"❌ Erro ao atualizar planilha: {e}")
                    emails_enviados += 1
            else:
                emails_com_erro += 1
    
    server.quit()
    
    # Relatório final
    print("\n📊 RELATÓRIO FINAL")
    print(f"✅ Emails enviados: {emails_enviados}")
    print(f"❌ Emails com erro: {emails_com_erro}")
    print(f"⏰ Concluído em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

if __name__ == "__main__":
    main()