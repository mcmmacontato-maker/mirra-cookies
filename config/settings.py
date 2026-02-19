"""Configurações da aplicação Mirra Cookies"""
import os
from dataclasses import dataclass

@dataclass
class EmailConfig:
    """Configurações de Email"""
    # ⚠️ IMPORTANTE: Configure as variáveis de ambiente no seu servidor
    SENDER_EMAIL = os.getenv("MIRRA_EMAIL", "seu-email@gmail.com")
    SENDER_PASSWORD = os.getenv("MIRRA_EMAIL_PASSWORD", "sua-senha-app-google")  # Use Google App Password
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    # Para Outlook:
    # SMTP_SERVER = "smtp.office365.com"
    # SMTP_PORT = 587

@dataclass
class AppConfig:
    """Configurações gerais da aplicação"""
    APP_NAME = "Mirra Cookies"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False") == "True"
    DATABASE_PATH = "database/mirra_cookies.db"
    SECRET_KEY = os.getenv("SECRET_KEY", "mirra-secret-2026-change-in-production")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "mirra_admin_2024")
    
    # Configurações de pagamento (Stripe/MercadoPago)
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")
    MERCADOPAGO_TOKEN = os.getenv("MERCADOPAGO_TOKEN", "")

@dataclass
class SecurityConfig:
    """Configurações de segurança"""
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_NUMBERS = True
    PASSWORD_REQUIRE_SPECIAL = True
    RECOVERY_CODE_EXPIRY_MINUTES = 15
    SESSION_TIMEOUT_MINUTES = 30
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 15

# Cupons de desconto
CUPONS_RECORRENTES = {
    "DOCE20": 0.20,
    "IMPERIAL30": 0.30,
    "PREMIUM40": 0.40,
    "MIRRA10": 0.10
}

# URLs de imagens com fallback mais confiável
PRODUCT_IMAGES = {
    "c1": "https://images.pexels.com/photos/312418/pexels-photo-312418.jpeg?w=600&q=80",
    "c2": "https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?w=600&q=80",
    "c3": "https://images.pexels.com/photos/1092730/pexels-photo-1092730.jpeg?w=600&q=80",
    "c4": "https://images.pexels.com/photos/821365/pexels-photo-821365.jpeg?w=600&q=80",
    "c5": "https://images.pexels.com/photos/1410235/pexels-photo-1410235.jpeg?w=600&q=80",
    "c6": "https://images.pexels.com/photos/1092730/pexels-photo-1092730.jpeg?w=600&q=80",
    "combo1": "https://images.pexels.com/photos/1092730/pexels-photo-1092730.jpeg?w=600&q=80",
}

# Fallback para quando as imagens não carregarem
FALLBACK_IMAGE = "https://via.placeholder.com/600x400?text=Mirra+Cookies"
