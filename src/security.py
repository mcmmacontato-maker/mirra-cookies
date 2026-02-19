"""Security and validation functions"""
import hashlib
import re
import secrets
from config.settings import SecurityConfig
from datetime import datetime, timedelta

class SecurityUtils:
    """Security utilities for password hashing, validation, etc"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256 + salt"""
        salt = secrets.token_hex(32)
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return f"{salt}${pwd_hash.hex()}"
    
    @staticmethod
    def verify_password(password, hashed):
        """Verify password against hash"""
        try:
            salt, pwd_hash = hashed.split('$')
            new_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return new_hash.hex() == pwd_hash
        except:
            # Fallback for old SHA-256 hashes (for migration)
            return hashlib.sha256(password.encode()).hexdigest() == hashed
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password_strength(password):
        """Validate password strength"""
        errors = []
        
        if len(password) < SecurityConfig.PASSWORD_MIN_LENGTH:
            errors.append(f"Mínimo {SecurityConfig.PASSWORD_MIN_LENGTH} caracteres")
        
        if SecurityConfig.PASSWORD_REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
            errors.append("Deve conter pelo menos 1 letra maiúscula")
        
        if SecurityConfig.PASSWORD_REQUIRE_NUMBERS and not re.search(r'\d', password):
            errors.append("Deve conter pelo menos 1 número")
        
        if SecurityConfig.PASSWORD_REQUIRE_SPECIAL and not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?]', password):
            errors.append("Deve conter pelo menos 1 caractere especial: !@#$%^&*()_+")
        
        return errors
    
    @staticmethod
    def generate_recovery_code():
        """Generate recovery code"""
        return secrets.token_urlsafe(6).replace('-', 'A').replace('_', 'B')[:6].upper()
    
    @staticmethod
    def get_recovery_code_expiry():
        """Get recovery code expiry time"""
        return datetime.now() + timedelta(minutes=SecurityConfig.RECOVERY_CODE_EXPIRY_MINUTES)
    
    @staticmethod
    def sanitize_input(text):
        """Remove potentially dangerous characters"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove script tags
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        return text.strip()
    
    @staticmethod
    def is_password_exposed(password):
        """Check if password is in common passwords list (simple check)"""
        common_passwords = [
            "password", "123456", "12345678", "qwerty", "abc123",
            "monkey", "1234567", "letmein", "trustno1", "dragon",
            "123123", "666666", "654321", "superman", "111111",
            "iloveyou", "master", "sunshine", "ashley", "bailey"
        ]
        return password.lower() in common_passwords
    
    @staticmethod
    def validate_credit_card(card_number):
        """Validate credit card using Luhn algorithm"""
        # Remove spaces and dashes
        card_number = card_number.replace(' ', '').replace('-', '')
        
        # Check if it's all digits
        if not card_number.isdigit():
            return False
        
        # Check length (most cards are 13-19 digits)
        if not (13 <= len(card_number) <= 19):
            return False
        
        # Luhn algorithm
        def luhn_checksum(card_num):
            def digits_of(n):
                return [int(d) for d in str(n)]
            
            digits = digits_of(card_num)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10
        
        return luhn_checksum(card_number) == 0
    
    @staticmethod
    def mask_credit_card(card_number):
        """Mask credit card for display (show only last 4 digits)"""
        card_number = card_number.replace(' ', '').replace('-', '')
        if len(card_number) >= 4:
            return 'X' * (len(card_number) - 4) + card_number[-4:]
        return 'INVALID'
    
    @staticmethod
    def validate_cvv(cvv):
        """Validate CVV (3 or 4 digits)"""
        return re.match(r'^\d{3,4}$', cvv) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validate Brazilian phone number"""
        # Remove special characters
        phone = re.sub(r'\D', '', phone)
        # Check if it has 11 digits (Brazilian format: 11 99999-9999)
        return len(phone) == 11


class DataValidator:
    """Data validation utilities"""
    
    @staticmethod
    def validate_name(name):
        """Validate name (no empty, no special chars)"""
        if not name or len(name.strip()) < 2:
            return False, "Nome deve ter pelo menos 2 caracteres"
        
        if not re.match(r"^[a-záéíóúâêôãõçñ\s'-]+$", name, re.IGNORECASE):
            return False, "Nome contém caracteres inválidos"
        
        return True, ""
    
    @staticmethod
    def validate_address(address):
        """Validate address"""
        if not address or len(address.strip()) < 10:
            return False, "Endereço muito curto (mínimo 10 caracteres)"
        
        if len(address.strip()) > 200:
            return False, "Endereço muito longo (máximo 200 caracteres)"
        
        return True, ""
    
    @staticmethod
    def validate_review_text(text):
        """Validate review text"""
        if not text or len(text.strip()) < 5:
            return False, "Comentário deve ter pelo menos 5 caracteres"
        
        if len(text.strip()) > 500:
            return False, "Comentário não pode ter mais de 500 caracteres"
        
        return True, ""
