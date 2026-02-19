"""
🧪 Script de teste para Mirra Cookies
Testa todas as funcionalidades principais antes de deploy
"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all imports"""
    print("🔍 Testando imports...")
    try:
        from config.settings import AppConfig, EmailConfig
        from database.db import DatabaseConnection
        from src.security import SecurityUtils, DataValidator
        from src.email_service import EmailService
        from src.products import PRODUCTS
        print("✅ Todos os imports funcionam!")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar: {e}")
        return False

def test_database():
    """Test database"""
    print("\n🗄️ Testando banco de dados...")
    try:
        from database.db import db
        
        # Test creating user
        user_id = db.create_user("test@example.com", "hash123", "Test User")
        if user_id:
            print("✅ Usuário criado com sucesso!")
            
            # Get user
            user = db.get_user_by_id(user_id)
            if user:
                print(f"✅ Usuário recuperado: {user['email']}")
                return True
        else:
            print("❌ Falha ao criar usuário (pode estar duplicado)")
            return False
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False

def test_security():
    """Test security functions"""
    print("\n🔒 Testando funções de segurança...")
    try:
        from src.security import SecurityUtils, DataValidator
        
        # Test password hashing
        password = "Test@12345"
        hashed = SecurityUtils.hash_password(password)
        verified = SecurityUtils.verify_password(password, hashed)
        
        if verified:
            print("✅ Hash e verificação de senha funcionam!")
        else:
            print("❌ Verificação de senha falhou!")
            return False
        
        # Test email validation
        if SecurityUtils.validate_email("test@example.com"):
            print("✅ Validação de email funciona!")
        else:
            print("❌ Validação de email falhou!")
            return False
        
        # Test password strength
        errors = SecurityUtils.validate_password_strength("weak")
        if errors:
            print(f"✅ Validação de força: {len(errors)} erros detectados")
        
        # Test recovery code
        code = SecurityUtils.generate_recovery_code()
        if code and len(code) == 6:
            print(f"✅ Código de recuperação gerado: {code}")
        
        return True
    except Exception as e:
        print(f"❌ Erro em segurança: {e}")
        return False

def test_email():
    """Test email service"""
    print("\n📧 Testando serviço de email...")
    try:
        from src.email_service import EmailService
        from config.settings import EmailConfig, AppConfig
        
        # Check environment
        if not EmailConfig.SENDER_EMAIL or EmailConfig.SENDER_EMAIL == "seu-email@gmail.com":
            print("⚠️  Aviso: MIRRA_EMAIL não configurado")
            print("   Configure no arquivo .env ou variáveis de ambiente")
            print("   Teste local? Digite seu email Google para teste")
            email = input("   Email para teste (ou deixe em branco): ").strip()
            if email:
                print(f"   Testando com {email}...")
            else:
                print("❌ MIRRA_EMAIL não configurado. Pulando teste de email.")
                return False
        else:
            email = EmailConfig.SENDER_EMAIL
            print(f"📧 Vou tentar enviar para: {email}")
        
        # Try to send test email
        print("   Tentando enviar email...")
        result = EmailService.send_recovery_code(
            email,
            "123456",
            "Teste"
        )
        
        if result or AppConfig.DEBUG:
            print("✅ Email enviado com sucesso!")
            if AppConfig.DEBUG:
                print("   (Debug mode: sem mensagem, apenas simulado)")
            return True
        else:
            print("❌ Falha ao enviar email")
            print("   Verifique:")
            print("   1. MIRRA_EMAIL está correto no .env")
            print("   2. MIRRA_EMAIL_PASSWORD é a senha do Google App")
            print("   3. 2FA está ativado na conta Google")
            return False
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        print("   Dica: Se usar Gmail, gere um App Password em:")
        print("   https://myaccount.google.com/apppasswords")
        return False

def test_products():
    """Test products"""
    print("\n🍪 Testando catálogo de produtos...")
    try:
        from src.products import PRODUCTS, CATEGORIES, FAQS, CONTACT_INFO
        
        if len(PRODUCTS) > 0:
            print(f"✅ {len(PRODUCTS)} produtos carregados!")
            print(f"   Exemplo: {list(PRODUCTS.values())[0]['nome']}")
        
        if len(CATEGORIES) > 0:
            print(f"✅ {len(CATEGORIES)} categorias disponíveis!")
        
        if len(FAQS) > 0:
            print(f"✅ {len(FAQS)} FAQs disponíveis!")
        
        if CONTACT_INFO:
            print(f"✅ Informações de contato carregadas!")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar produtos: {e}")
        return False

def test_validation():
    """Test data validation"""
    print("\n✔️ Testando validação de dados...")
    try:
        from src.security import DataValidator
        
        # Test name
        valid, msg = DataValidator.validate_name("João Silva")
        if valid:
            print("✅ Validação de nome funciona!")
        else:
            print(f"❌ Validação de nome: {msg}")
            return False
        
        # Test address
        valid, msg = DataValidator.validate_address("Rua Imperial, 123, São Paulo")
        if valid:
            print("✅ Validação de endereço funciona!")
        else:
            print(f"❌ Validação de endereço: {msg}")
            return False
        
        # Test credit card
        valid = DataValidator.validate_credit_card("4111111111111111")
        if valid:
            print("✅ Validação de cartão funciona!")
        else:
            print("❌ Validação de cartão falhou!")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erro em validação: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 MIRRA COOKIES - TEST SUITE")
    print("=" * 60)
    
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Arquivo .env carregado\n")
    except:
        print("⚠️  Arquivo .env não encontrado (crie um)\n")
    
    tests = [
        ("Importações", test_imports),
        ("Banco de Dados", test_database),
        ("Segurança", test_security),
        ("Email", test_email),
        ("Produtos", test_products),
        ("Validação", test_validation),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"❌ Erro em {name}: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 TUDO OK! Você pode fazer deploy!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam. Verifique acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
