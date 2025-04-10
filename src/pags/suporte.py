import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
from database import Database


# Carrega variáveis do .env
load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE", "")
SENHA = os.getenv("SENHA", "")
EMAILS_DESTINO = os.getenv("EMAILS_DESTINO", "").split(",") if os.getenv("EMAILS_DESTINO") else []
SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PORTA = 587

class Suporte:
    def show(self):
        st.title("📨 Suporte do Terminal")
        st.write("Use o formulário abaixo para relatar um problema ou dúvida.")

        user_tipo = st.session_state["auth_user"]["tipo"]
        user_id = st.session_state["auth_user"]["id"]
        user_email = st.session_state["auth_user"]["email"]
        user_name = st.session_state["auth_user"]["nome"]
        mensagem = st.text_area("Descreva seu problema ou dúvida:")
        Anexo = st.file_uploader("Enviar arquivos (se necessário)", type=["jpg", "jpeg", "pdf","png","webp"], accept_multiple_files=True)


        if st.button("Enviar Mensagem"):
            if not mensagem:
                st.error("❗ Preencha todos os campos antes de enviar.")
            else:
                assunto = f"Mensagem de {user_name} - ID: {user_id} - Tipo: {user_tipo}"
                corpo = f"""
E-mail: {user_email}

Mensagem:
{mensagem}
                """
                sucesso = self.send_email(assunto, corpo, Anexo)
                if sucesso:
                    st.success("✅ Mensagem enviada com sucesso!")
                    st.balloons()
                else:
                    st.error("❌ Erro ao enviar a mensagem. Caso seja urgente, contate-nos via telefone: (13) XXXX-XXXX.")

    def send_email(self, assunto, corpo, anexos):
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = ", ".join(EMAILS_DESTINO)
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo, 'plain'))

        # Adiciona os anexos
        if anexos:
            for anexo in anexos:
                try:
                    anexo_bytes = anexo.read()
                    anexo_nome = anexo.name
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(anexo_bytes)
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{anexo_nome}"')
                    msg.attach(part)
                except Exception as e:
                    print(f"Erro ao anexar arquivo {anexo.name}: {e}")

        try:
            server = smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA)
            server.starttls()
            server.login(EMAIL_REMETENTE, SENHA)
            server.sendmail(EMAIL_REMETENTE, EMAILS_DESTINO, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print("Erro ao enviar e-mail:", e)
            return False