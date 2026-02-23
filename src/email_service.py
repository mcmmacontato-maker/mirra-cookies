"""Email service for password recovery and notifications"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import EmailConfig, AppConfig
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails"""
    @staticmethod
    def _validate_config():
        """Validate email configuration and return (is_valid, message)"""
        if not EmailConfig.SENDER_EMAIL or EmailConfig.SENDER_EMAIL == "seu-email@gmail.com":
            return False, "remetente (MIRRA_EMAIL) não configurado"
        if not EmailConfig.SENDER_PASSWORD or EmailConfig.SENDER_PASSWORD == "sua-senha-app-google":
            return False, "senha do remetente (MIRRA_EMAIL_PASSWORD) não configurada - use Senha de App do Google"
        return True, ""
    
    @staticmethod
    def send_recovery_code(recipient_email, recovery_code, user_name="Visitante"):
        """Send password recovery code via email"""
        valid, msg = EmailService._validate_config()
        if not valid:
            logger.error(f"Configuração de e-mail inválida: {msg}")
            return False

        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = "🍪 Código de Recuperação - Mirra Cookies"
            message['From'] = EmailConfig.SENDER_EMAIL
            message['To'] = recipient_email
            
            # HTML content
            html_content = f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: 'Poppins', sans-serif; background-color: #fdfaf7; }}
                        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                        .header {{ background: linear-gradient(135deg, #3d2817 0%, #5a3d2a 100%); 
                                   color: #fdfaf7; padding: 30px; border-radius: 10px; text-align: center; }}
                        .content {{ background: white; padding: 30px; border-radius: 10px; margin-top: 20px; }}
                        .code-box {{ background: #f0e6e0; padding: 20px; border-radius: 8px; 
                                     text-align: center; font-size: 24px; font-weight: bold; 
                                     color: #3d2817; letter-spacing: 4px; margin: 20px 0; }}
                        .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
                        .warning {{ color: #d32f2f; font-weight: bold; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>🍪 MIRRA COOKIES</h1>
                            <p>Recuperação de Senha</p>
                        </div>
                        
                        <div class="content">
                            <h2>Olá {user_name}!</h2>
                            <p>Você solicitou a recuperação de sua senha na Mirra Cookies.</p>
                            
                            <p><strong>Seu código de recuperação é:</strong></p>
                            <div class="code-box">{recovery_code}</div>
                            
                            <p>️⚠️ <span class="warning">Este código expira em 15 minutos.</span></p>
                            <p>⚠️ <span class="warning">Nunca compartilhe este código com ninguém.</span></p>
                            
                            <hr style="border: none; border-top: 1px solid #f0e6e0; margin: 20px 0;">
                            
                            <p style="color: #666; font-size: 14px;">
                                Se você não solicitou a recuperação de senha, ignore este e-mail e sua conta permanecerá segura.
                            </p>
                        </div>
                        
                        <div class="footer">
                            <p>© 2026 Mirra Cookies | Premium Artisan Cookies</p>
                            <p>Desenvolvido com ❤️</p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            # Plain text version
            text_content = f"""
            Olá {user_name}!
            
            Você solicitou a recuperação de sua senha na Mirra Cookies.
            
            Seu código de recuperação é: {recovery_code}
            
            ⚠️ Este código expira em 15 minutos.
            ⚠️ Nunca compartilhe este código com ninguém.
            
            Se você não solicitou a recuperação de senha, ignore este e-mail.
            
            © 2026 Mirra Cookies | Premium Artisan Cookies
            """
            
            # Attach both versions
            message.attach(MIMEText(text_content, 'plain'))
            message.attach(MIMEText(html_content, 'html'))
            
            # Send email
            with smtplib.SMTP(EmailConfig.SMTP_SERVER, EmailConfig.SMTP_PORT) as server:
                server.starttls()
                server.login(EmailConfig.SENDER_EMAIL, EmailConfig.SENDER_PASSWORD)
                server.send_message(message)
            
            logger.info(f"Recovery code email sent to {recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"Autenticação SMTP falhou: verifique MIRRA_EMAIL e MIRRA_EMAIL_PASSWORD. {e}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"Erro SMTP ao enviar e-mail: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending recovery email: {str(e)}")
            if AppConfig.DEBUG:
                logger.warning(f"DEBUG MODE: Email would be sent to {recipient_email} with code {recovery_code}")
                return True
            return False
    
    @staticmethod
    def send_order_confirmation(recipient_email, order_number, order_total, user_name="Visitante"):
        """Send order confirmation email"""
        try:
            valid, msg = EmailService._validate_config()
            if not valid:
                logger.error(f"Configuração de e-mail inválida: {msg}")
                return False

            message = MIMEMultipart('alternative')
            message['Subject'] = f"🍪 Pedido Confirmado #{order_number} - Mirra Cookies"
            message['From'] = EmailConfig.SENDER_EMAIL
            message['To'] = recipient_email
            
            html_content = f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: 'Poppins', sans-serif; background-color: #fdfaf7; }}
                        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                        .header {{ background: linear-gradient(135deg, #3d2817 0%, #5a3d2a 100%); 
                                   color: #fdfaf7; padding: 30px; border-radius: 10px; text-align: center; }}
                        .content {{ background: white; padding: 30px; border-radius: 10px; margin-top: 20px; }}
                        .order-info {{ background: #d4edda; padding: 15px; border-radius: 8px; margin: 15px 0; }}
                        .total {{ font-size: 20px; font-weight: bold; color: #3d2817; }}
                        .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>🍪 MIRRA COOKIES</h1>
                            <p>Pedido Confirmado!</p>
                        </div>
                        
                        <div class="content">
                            <h2>Ótimo, {user_name}!</h2>
                            <p>Seu pedido foi confirmado com sucesso!</p>
                            
                            <div class="order-info">
                                <p><strong>Número do Pedido:</strong> {order_number}</p>
                                <p><span class="total">Total: R$ {order_total:.2f}</span></p>
                            </div>
                            
                            <p>📦 Seu pedido está sendo preparado e será entregue em até 48 horas úteis.</p>
                            <p>📧 Você receberá uma mensagem de atualização quando seu pedido for enviado.</p>
                            
                            <hr style="border: none; border-top: 1px solid #f0e6e0; margin: 20px 0;">
                            
                            <p style="color: #666; font-size: 14px;">
                                Obrigado por escolher Mirra Cookies! 🍪❤️
                            </p>
                        </div>
                        
                        <div class="footer">
                            <p>© 2026 Mirra Cookies | Premium Artisan Cookies</p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            text_content = f"""
            Ótimo, {user_name}!
            
            Seu pedido foi confirmado com sucesso!
            
            Número do Pedido: {order_number}
            Total: R$ {order_total:.2f}
            
            📦 Seu pedido está sendo preparado e será entregue em até 48 horas úteis.
            
            Obrigado por escolher Mirra Cookies! 🍪❤️
            
            © 2026 Mirra Cookies | Premium Artisan Cookies
            """
            
            message.attach(MIMEText(text_content, 'plain'))
            message.attach(MIMEText(html_content, 'html'))
            
            with smtplib.SMTP(EmailConfig.SMTP_SERVER, EmailConfig.SMTP_PORT) as server:
                server.starttls()
                server.login(EmailConfig.SENDER_EMAIL, EmailConfig.SENDER_PASSWORD)
                server.send_message(message)

            logger.info(f"Order confirmation email sent to {recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"Autenticação SMTP falhou: {e}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"Erro SMTP ao enviar confirmação de pedido: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending order confirmation: {str(e)}")
            return False
    
    @staticmethod
    def send_contact_form_notification(sender_name, sender_email, subject, message_text):
        """Send contact form notification to admin"""
        try:
            valid, msg = EmailService._validate_config()
            if not valid:
                logger.error(f"Configuração de e-mail inválida: {msg}")
                return False

            message = MIMEMultipart('alternative')
            message['Subject'] = f"📧 Nova Mensagem de Contato: {subject}"
            message['From'] = EmailConfig.SENDER_EMAIL
            message['To'] = EmailConfig.SENDER_EMAIL  # Admin email
            
            html_content = f"""
            <html>
                <body style="font-family: Poppins, sans-serif;">
                    <h2>📧 Nova Mensagem de Contato</h2>
                    <p><strong>De:</strong> {sender_name}</p>
                    <p><strong>Email:</strong> {sender_email}</p>
                    <p><strong>Assunto:</strong> {subject}</p>
                    <hr>
                    <p><strong>Mensagem:</strong></p>
                    <p style="white-space: pre-wrap;">{message_text}</p>
                </body>
            </html>
            """
            
            message.attach(MIMEText(html_content, 'html'))
            
            with smtplib.SMTP(EmailConfig.SMTP_SERVER, EmailConfig.SMTP_PORT) as server:
                server.starttls()
                server.login(EmailConfig.SENDER_EMAIL, EmailConfig.SENDER_PASSWORD)
                server.send_message(message)

            logger.info(f"Contact form notification sent from {sender_email}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"Autenticação SMTP falhou: {e}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"Erro SMTP ao enviar notificação de contato: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending contact notification: {str(e)}")
            return False
