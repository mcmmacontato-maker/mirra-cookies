"""
🍪 MIRRA COOKIES - Premium Artisan Cookies
Main Application using Streamlit
Refactored with modular architecture and enhanced security
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import logging
from functools import wraps

# Import custom modules
from config.settings import AppConfig, SecurityConfig, EmailConfig, CUPONS_RECORRENTES
from database.db import db
from src.security import SecurityUtils, DataValidator
from src.email_service import EmailService
from src.products import PRODUCTS, CATEGORIES, FAQS, CONTACT_INFO, ABOUT_TEXT, POLICIES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Mirra Cookies | Premium",
    page_icon="🍪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize session state variables"""
    if 'cart' not in st.session_state:
        st.session_state.cart = {}
    if 'wishlist' not in st.session_state:
        st.session_state.wishlist = []
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = ""
    if 'desconto_aplicado' not in st.session_state:
        st.session_state.desconto_aplicado = 0.0
    if 'recovery_code' not in st.session_state:
        st.session_state.recovery_code = None
    if 'page' not in st.session_state:
        st.session_state.page = "cardapio"
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = {}

init_session_state()

# ============================================================================
# CSS STYLING
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #fdfaf7 0%, #f5f1ed 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #3d2817;
    }
    
    .header-title {
        text-align: center;
        font-family: 'Playfair Display', serif;
        font-size: 3.5em;
        color: #3d2817;
        margin: 1.5rem 0;
        letter-spacing: 2px;
    }
    
    .tagline {
        text-align: center;
        color: #8b6f47;
        font-size: 1.1em;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    .product-card {
        background: white;
        border-radius: 25px;
        padding: 1.5rem;
        border: 2px solid #f0e6e0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        text-align: center;
        min-height: 520px;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .product-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.12);
        border-color: #d4a373;
    }
    
    .product-image {
        width: 100%;
        border-radius: 20px;
        height: 200px;
        object-fit: cover;
        margin-bottom: 0.8rem;
    }
    
    .product-name {
        font-size: 1.3em;
        font-weight: 600;
        color: #3d2817;
        margin: 0.5rem 0;
    }
    
    .product-desc {
        font-size: 0.9rem;
        color: #666;
        margin: 0.8rem 0;
        line-height: 1.5;
    }
    
    .price-tag {
        color: #d4a373;
        font-weight: 700;
        font-size: 1.5rem;
        margin: 1rem 0;
    }
    
    .rating {
        color: #ffc107;
        font-size: 1rem;
        margin: 0.5rem 0;
    }
    
    .footer {
        background: linear-gradient(135deg, #3d2817 0%, #5a3d2a 100%);
        color: #fdfaf7;
        padding: 3rem 2rem;
        margin-top: 4rem;
        text-align: center;
        border-radius: 20px;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }
    
    .footer-link {
        color: #f0e6e0;
        text-decoration: none;
        font-size: 0.95rem;
    }
    
    .about-box {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 5px solid #d4a373;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }
    
    .review-card {
        background: #fdfaf7;
        border-left: 4px solid #d4a373;
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    
    .order-card {
        background: white;
        border-left: 5px solid #d4a373;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .status-processando {
        background-color: #fff3cd;
        color: #856404;
    }
    
    .status-enviado {
        background-color: #d4edda;
        color: #155724;
    }
    
    .status-entregue {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# AUTHENTICATION & SECURITY FUNCTIONS
# ============================================================================

def check_login_attempts(email):
    """Check and limit login attempts"""
    if email not in st.session_state.login_attempts:
        st.session_state.login_attempts[email] = {"count": 0, "locked_until": None}
    
    attempts = st.session_state.login_attempts[email]
    
    if attempts["locked_until"] and datetime.now() < attempts["locked_until"]:
        remaining = (attempts["locked_until"] - datetime.now()).seconds // 60
        return False, f"Conta temporariamente bloqueada. Tente novamente em {remaining} minutos."
    
    if attempts["locked_until"]:
        attempts["count"] = 0
        attempts["locked_until"] = None
    
    return True, ""

def record_login_failure(email):
    """Record failed login attempt"""
    attempts = st.session_state.login_attempts[email]
    attempts["count"] += 1
    
    if attempts["count"] >= SecurityConfig.MAX_LOGIN_ATTEMPTS:
        attempts["locked_until"] = datetime.now() + timedelta(
            minutes=SecurityConfig.LOCKOUT_DURATION_MINUTES
        )
        logger.warning(f"Account locked due to failed login attempts: {email}")

def sidebar_authentication():
    """Sidebar authentication UI"""
    with st.sidebar:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 🍪 **MIRRA COOKIES**")
        
        st.divider()
        
        if not st.session_state.logged_in:
            aba_auth = st.tabs(["🔓 Login", "📝 Cadastro"])
            
            with aba_auth[0]:
                st.write("**Acesse sua conta:**")
                email_log = st.text_input("📧 E-mail", key="email_log")
                senha_log = st.text_input("🔐 Senha", type="password", key="senha_log")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Entrar", use_container_width=True):
                        if not email_log:
                            st.error("❌ Digite seu e-mail.")
                        else:
                            can_attempt, message = check_login_attempts(email_log)
                            if not can_attempt:
                                st.error(message)
                            else:
                                user = db.get_user_by_email(email_log)
                                if user and SecurityUtils.verify_password(senha_log, user['password_hash']):
                                    st.session_state.logged_in = True
                                    st.session_state.user_email = email_log
                                    st.session_state.login_attempts[email_log] = {"count": 0, "locked_until": None}
                                    db.add_audit_log(user['id'], "LOGIN", {"ip": "local"})
                                    st.success("✅ Login realizado!")
                                    st.rerun()
                                else:
                                    record_login_failure(email_log)
                                    st.error("❌ E-mail ou senha incorretos.")
                
                with col2:
                    if st.button("🆘 Esqueci", use_container_width=True):
                        if email_log:
                            if not SecurityUtils.validate_email(email_log):
                                st.error("❌ E-mail inválido.")
                            else:
                                user = db.get_user_by_email(email_log)
                                if user:
                                    # Generate recovery code
                                    codigo_recuperacao = SecurityUtils.generate_recovery_code()
                                    expiry = SecurityUtils.get_recovery_code_expiry()
                                    db.create_recovery_code(user['id'], codigo_recuperacao, expiry)
                                    
                                    # Send email
                                    email_sent = EmailService.send_recovery_code(
                                        email_log,
                                        codigo_recuperacao,
                                        user['name']
                                    )
                                    
                                    if email_sent or AppConfig.DEBUG:
                                        st.session_state.recovery_code = codigo_recuperacao
                                        st.success("✅ Código enviado para seu e-mail!")
                                        st.info(f"📧 Verifique: {email_log}")
                                        if AppConfig.DEBUG:
                                            st.warning(f"DEBUG: Código = {codigo_recuperacao}")
                                    else:
                                        st.error("❌ Erro ao enviar código. Verifique suas configurações de email.")
                                else:
                                    st.warning("E-mail não encontrado.")
                        else:
                            st.warning("Digite seu e-mail.")
                
                if st.session_state.recovery_code:
                    st.divider()
                    st.write("**Redefinir Senha:**")
                    tentativa = st.text_input("Código do e-mail", key="recovery_input")
                    nova_senha_reset = st.text_input("Nova senha", type="password", key="new_pass_reset")
                    nova_senha_reset_conf = st.text_input("Confirmar", type="password", key="new_pass_reset_conf")
                    
                    if st.button("✅ Redefinir"):
                        if tentativa != st.session_state.recovery_code:
                            st.error("❌ Código incorreto.")
                        elif nova_senha_reset != nova_senha_reset_conf:
                            st.error("❌ Senhas não correspondem.")
                        else:
                            errors = SecurityUtils.validate_password_strength(nova_senha_reset)
                            if errors:
                                for error in errors:
                                    st.error(f"❌ {error}")
                            elif SecurityUtils.is_password_exposed(nova_senha_reset):
                                st.error("❌ Senha muito comum. Escolha outra.")
                            else:
                                user = db.get_user_by_email(email_log)
                                if user:
                                    new_hash = SecurityUtils.hash_password(nova_senha_reset)
                                    db.update_password(user['id'], new_hash)
                                    db.add_audit_log(user['id'], "PASSWORD_RESET", {})
                                    st.success("✅ Senha redefinida com sucesso!")
                                    st.session_state.recovery_code = None
                                    st.rerun()
            
            with aba_auth[1]:
                st.write("**Crie sua conta:**")
                novo_nome = st.text_input("👤 Nome Completo", key="signup_name")
                novo_email = st.text_input("📧 E-mail", key="signup_email")
                nova_senha = st.text_input("🔐 Criar Senha", type="password", key="signup_pass")
                nova_senha_conf = st.text_input("🔐 Confirmar", type="password", key="signup_pass_conf")
                
                if st.button("✨ Criar Conta", use_container_width=True):
                    # Validations
                    if not novo_email or not nova_senha or not novo_nome:
                        st.error("❌ Preencha todos os campos.")
                    elif not SecurityUtils.validate_email(novo_email):
                        st.error("❌ E-mail inválido!")
                    elif db.get_user_by_email(novo_email):
                        st.error("❌ E-mail já cadastrado!")
                    elif nova_senha != nova_senha_conf:
                        st.error("❌ Senhas não correspondem.")
                    else:
                        errors = SecurityUtils.validate_password_strength(nova_senha)
                        valid_name, name_error = DataValidator.validate_name(novo_nome)
                        
                        if not valid_name:
                            st.error(f"❌ {name_error}")
                        elif errors:
                            for error in errors:
                                st.error(f"❌ {error}")
                        elif SecurityUtils.is_password_exposed(nova_senha):
                            st.error("❌ Senha muito comum. Escolha outra.")
                        else:
                            password_hash = SecurityUtils.hash_password(nova_senha)
                            user_id = db.create_user(novo_email, password_hash, novo_nome)
                            
                            if user_id:
                                db.add_audit_log(user_id, "ACCOUNT_CREATED", {"method": "email"})
                                st.success("✅ Conta criada com sucesso!")
                                st.info("🎉 Bem-vindo! Faça login.")
                            else:
                                st.error("❌ Erro ao criar conta.")
        else:
            user = db.get_user_by_id(
                db.get_user_by_email(st.session_state.user_email)['id']
            )
            
            if user:
                st.markdown(f"""
                <div class='about-box'>
                    <h3>👑 {user['name']}</h3>
                    <p style='font-size: 0.9rem; color: #666;'>
                    📧 {user['email']}<br>
                    📅 Membro desde {user['created_at'][:10]}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.divider()
                
                if st.button("🚪 Sair", use_container_width=True):
                    db.add_audit_log(user['id'], "LOGOUT", {})
                    st.session_state.logged_in = False
                    st.session_state.cart = {}
                    st.session_state.wishlist = []
                    st.session_state.desconto_aplicado = 0.0
                    st.rerun()

# ============================================================================
# PRODUCT DISPLAY
# ============================================================================

def display_products(product_filter=None):
    """Display products in grid"""
    st.markdown("### 👨‍🍳 Nossas Especialidades")
    
    cols = st.columns(3)
    for i, (p_id, p) in enumerate(PRODUCTS.items()):
        if product_filter and p.get("categoria") != product_filter:
            continue
        
        with cols[i % 3]:
            st.markdown(f"""
                <div class="product-card">
                    <img src="{p['img']}" class="product-image" alt="{p['nome']}" onerror="this.src='https://via.placeholder.com/600x400?text={p['nome']}'">
                    <div class="product-name">{p['nome']}</div>
                    <div class="product-desc">{p['desc']}</div>
                    <div class="rating">⭐ {p['rating']}/5.0</div>
                    <div class="price-tag">R$ {p['preco']:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🛒 Adicionar", key=f"btn_{p_id}", use_container_width=True):
                    if st.session_state.logged_in:
                        if p_id in st.session_state.cart:
                            st.session_state.cart[p_id]['qty'] += 1
                        else:
                            st.session_state.cart[p_id] = {**p, 'qty': 1}
                        st.toast(f"✅ {p['nome']} adicionado à sacola!")
                    else:
                        st.error("Faça login para adicionar à sacola!")
            
            with col2:
                if st.button(f"❤️", key=f"wish_{p_id}", use_container_width=True):
                    if st.session_state.logged_in:
                        if p_id not in st.session_state.wishlist:
                            st.session_state.wishlist.append(p_id)
                            st.toast("❤️ Adicionado aos favoritos!")
                        else:
                            st.session_state.wishlist.remove(p_id)
                            st.toast("💔 Removido dos favoritos!")
                    else:
                        st.error("Faça login para usar favoritos!")
            
            with st.expander(f"📋 {p['nome']}"):
                st.write(f"**Ingredientes:** {p['ingredientes']}")
                st.write(f"**Alergênios:** {p['alergênios']}")
                st.write(f"**Tamanho:** {p['tamanho']}")
                
                # Reviews
                reviews = db.get_product_reviews(p_id)
                if reviews:
                    st.write("**Avaliações:**")
                    for rev in reviews:
                        st.markdown(f"""
                        <div class="review-card">
                            <b>{rev['name']}</b> - {'⭐' * rev['rating']}<br>
                            {rev['text']}<br>
                            <small>{rev['created_at'][:10]}</small>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Add review if logged in
                if st.session_state.logged_in:
                    with st.form(f"review_{p_id}"):
                        nota_rev = st.slider("Sua nota:", 1, 5, 5, key=f"nota_{p_id}")
                        texto_rev = st.text_area("Comentário:", key=f"texto_{p_id}", height=80)
                        if st.form_submit_button("📤 Enviar Avaliação"):
                            valid_review, error = DataValidator.validate_review_text(texto_rev)
                            if not valid_review:
                                st.error(f"❌ {error}")
                            else:
                                user = db.get_user_by_email(st.session_state.user_email)
                                db.add_review(p_id, user['id'], nota_rev, texto_rev)
                                st.success("✅ Avaliação enviada com sucesso!")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application"""
    
    # Sidebar authentication
    sidebar_authentication()
    
    # Main header
    st.markdown("<div class='header-title'>🍪 MIRRA COOKIES</div>", unsafe_allow_html=True)
    st.markdown("<div class='tagline'>✨ Premium Artisan Cookies | Qualidade Imperial ✨</div>", unsafe_allow_html=True)
    
    # Main tabs
    tab_menu, tab_cart, tab_pages, tab_admin = st.tabs(["🛍️ CARDÁPIO", "🛒 SACOLA", "ℹ️ MAIS", "🔐 ADMIN"])
    
    # ========================================================================
    # TAB 1: MENU
    # ========================================================================
    with tab_menu:
        categoria = st.selectbox(
            "Filtrar por categoria:",
            ["Todos"] + list(CATEGORIES.keys())
        )
        filter_cat = None if categoria == "Todos" else categoria
        display_products(filter_cat)
    
    # ========================================================================
    # TAB 2: CART
    # ========================================================================
    with tab_cart:
        if not st.session_state.logged_in:
            st.warning("⚠️ Faça login para acessar a sacola.")
        elif not st.session_state.cart:
            st.info("🛒 Sua sacola está vazia.")
        else:
            st.markdown("### 🛒 Sua Sacola")
            
            total_bruto = 0
            for p_id, item in list(st.session_state.cart.items()):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"**{item['nome']}**")
                with col2:
                    qty = st.number_input(f"Qtd", 1, 100, item['qty'], key=f"qty_{p_id}")
                    st.session_state.cart[p_id]['qty'] = qty
                with col3:
                    st.write(f"R$ {item['preco'] * qty:.2f}")
                with col4:
                    if st.button("🗑️", key=f"del_{p_id}"):
                        del st.session_state.cart[p_id]
                        st.rerun()
                
                total_bruto += item['preco'] * item['qty']
            
            st.divider()
            
            user = db.get_user_by_email(st.session_state.user_email)
            if user:
                # Cupom section
                with st.expander("🎟️ Cupom de Desconto"):
                    cupom = st.text_input("Código:").upper()
                    if st.button("✓ Validar", use_container_width=True):
                        if cupom == "MIRRA10":
                            # First order discount
                            orders = db.get_user_orders(user['id'])
                            if len(orders) == 0:
                                st.session_state.desconto_aplicado = total_bruto * 0.10
                                st.success("✅ 10% OFF - 1ª Compra!")
                            else:
                                st.error("❌ Este cupom é apenas para primeira compra.")
                        elif cupom in CUPONS_RECORRENTES:
                            # Recurring discount check
                            last_used = db.get_last_cupom_usage(user['id'], cupom)
                            if last_used is None:
                                desconto = CUPONS_RECORRENTES[cupom]
                                st.session_state.desconto_aplicado = total_bruto * desconto
                                st.success(f"✅ {int(desconto*100)}% OFF!")
                            else:
                                try:
                                    last_date = datetime.fromisoformat(last_used)
                                    dias = (datetime.now() - last_date).days
                                    if dias >= 30:
                                        desconto = CUPONS_RECORRENTES[cupom]
                                        st.session_state.desconto_aplicado = total_bruto * desconto
                                        st.success(f"✅ {int(desconto*100)}% OFF!")
                                    else:
                                        st.warning(f"⏳ Cupom disponível em {30-dias} dias")
                                except:
                                    st.error("❌ Cupom inválido.")
                        else:
                            st.error("❌ Cupom não encontrado.")
                
                st.divider()
                
                # Total and checkout
                total_final = total_bruto - st.session_state.desconto_aplicado
                if st.session_state.desconto_aplicado > 0:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Subtotal:** R$ {total_bruto:.2f}")
                    with col2:
                        st.write(f"**Desconto:** -R$ {st.session_state.desconto_aplicado:.2f}")
                    st.markdown(f"## 💰 Total: R$ {total_final:.2f}")
                else:
                    st.markdown(f"## 💰 Total: R$ {total_final:.2f}")
                
                # Checkout form
                with st.form("checkout"):
                    st.write("### 📦 Entrega")
                    nome_ent = st.text_input("Nome", value=user['name'])
                    end = st.text_area("Endereço completo")
                    
                    st.write("### 💳 Pagamento")
                    metodo = st.selectbox("Método:", ["PIX", "Crédito", "Débito", "Dinheiro (reembolso)"])
                    
                    if metodo in ["Crédito", "Débito"]:
                        st.warning("⚠️ IMPORTANTE: Seus dados de cartão serão processados com segurança. Nunca salvamos números de cartão completos.")
                        num_cartao = st.text_input("Cartão (16 dígitos)", max_chars=19)
                        col1, col2 = st.columns(2)
                        with col1:
                            validade = st.text_input("Validade (MM/AA)")
                        with col2:
                            cvv = st.text_input("CVV", type="password", max_chars=4)
                    
                    if st.form_submit_button("✅ FINALIZAR PEDIDO", use_container_width=True):
                        # Validations
                        valid_addr, addr_error = DataValidator.validate_address(end)
                        
                        if not valid_addr:
                            st.error(f"❌ {addr_error}")
                        elif metodo in ["Crédito", "Débito"]:
                            if not SecurityUtils.validate_credit_card(num_cartao):
                                st.error("❌ Número de cartão inválido.")
                            elif not SecurityUtils.validate_cvv(cvv):
                                st.error("❌ CVV inválido (3 ou 4 dígitos).")
                            else:
                                # Process order
                                num_pedido = f"MRR-{random.randint(100000, 999999)}"
                                
                                db.create_order(
                                    user['id'],
                                    num_pedido,
                                    st.session_state.cart,
                                    total_final,
                                    st.session_state.desconto_aplicado,
                                    end,
                                    metodo
                                )
                                
                                # Log cupom if used
                                if st.session_state.desconto_aplicado > 0:
                                    # Find which cupom was used (simplified)
                                    db.log_cupom_usage(user['id'], "APPLIED")
                                
                                # Send confirmation email
                                EmailService.send_order_confirmation(
                                    user['email'],
                                    num_pedido,
                                    total_final,
                                    user['name']
                                )
                                
                                db.add_audit_log(user['id'], "ORDER_CREATED", {"order_number": num_pedido})
                                
                                st.success("✅ Pedido finalizado com sucesso!")
                                st.info(f"📦 **Número do Pedido: {num_pedido}**\n💚 Total: R$ {total_final:.2f}\n📍 Seu pedido está sendo preparado!")
                                
                                st.session_state.cart = {}
                                st.session_state.desconto_aplicado = 0.0
                        else:
                            # Non-credit card payment
                            num_pedido = f"MRR-{random.randint(100000, 999999)}"
                            
                            db.create_order(
                                user['id'],
                                num_pedido,
                                st.session_state.cart,
                                total_final,
                                st.session_state.desconto_aplicado,
                                end,
                                metodo
                            )
                            
                            EmailService.send_order_confirmation(
                                user['email'],
                                num_pedido,
                                total_final,
                                user['name']
                            )
                            
                            db.add_audit_log(user['id'], "ORDER_CREATED", {"order_number": num_pedido})
                            
                            st.success("✅ Pedido finalizado com sucesso!")
                            st.info(f"📦 **Número do Pedido: {num_pedido}**\n💚 Total: R$ {total_final:.2f}\n📍 Seu pedido está sendo preparado!")
                            
                            st.session_state.cart = {}
                            st.session_state.desconto_aplicado = 0.0
    
    # ========================================================================
    # TAB 3: MORE INFO
    # ========================================================================
    with tab_pages:
        sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5 = st.tabs(["📖 Sobre", "📋 Pedidos", "❓ FAQ", "📞 Contato", "📋 Políticas"])
        
        with sub_tab1:
            st.markdown(f"""
            <div class="about-box">
                <h2>🍪 Sobre Mirra Cookies</h2>
                <p>{ABOUT_TEXT}</p>
                <h3>✨ Nossa Missão</h3>
                <p>Criar experiências deliciosas com qualidade imperial e ingredientes selecionados.</p>
                <h3>🎯 Valores</h3>
                <ul>
                <li><b>Qualidade:</b> Melhores ingredientes importados</li>
                <li><b>Autenticidade:</b> Receitas caseiras e artesanais</li>
                <li><b>Sustentabilidade:</b> Embalagens eco-friendly</li>
                <li><b>Satisfação:</b> 100% comprometido com você</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with sub_tab2:
            if st.session_state.logged_in:
                user = db.get_user_by_email(st.session_state.user_email)
                orders = db.get_user_orders(user['id'])
                
                if orders:
                    st.markdown("### 📦 Seus Pedidos")
                    for order in orders:
                        data_pedido = datetime.fromisoformat(order['created_at']).strftime("%d/%m/%Y %H:%M")
                        st.markdown(f"""
                        <div class="order-card">
                            <b>{order['order_number']}</b> - {data_pedido}<br>
                            <span class="status-badge status-{order['status'].split()[0].lower()}">
                                {order['status']}
                            </span><br>
                            <b>R$ {order['total']:.2f}</b> | 📍 {order['address'][:40]}...
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander(f"Ver itens - {order['order_number']}"):
                            import json
                            items = json.loads(order['items'])
                            for p_id, item in items.items():
                                st.write(f"• {item['nome']} x{item.get('qty', 1)} - R$ {item['preco'] * item.get('qty', 1):.2f}")
                else:
                    st.info("📭 Nenhum pedido ainda.")
            else:
                st.warning("Faça login para ver seus pedidos.")
        
        with sub_tab3:
            st.markdown("## ❓ Perguntas Frequentes")
            for pergunta, resposta in FAQS:
                with st.expander(f"**{pergunta}**"):
                    st.write(resposta)
        
        with sub_tab4:
            st.markdown("## 📞 Entre em Contato")
            st.markdown(f"""
            <div class="about-box">
                <p><b>📍 Endereço:</b> {CONTACT_INFO['address']}</p>
                <p><b>📧 E-mail:</b> {CONTACT_INFO['email']}</p>
                <p><b>📱 WhatsApp:</b> {CONTACT_INFO['whatsapp']}</p>
                <p><b>📷 Instagram:</b> {CONTACT_INFO['instagram']}</p>
                <p><b>🕐 Horário:</b><br>
                Seg-Sex: {CONTACT_INFO['hours']['segunda_sexta']}<br>
                Sáb: {CONTACT_INFO['hours']['sabado']}<br>
                Dom: {CONTACT_INFO['hours']['domingo']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("contact_form"):
                nome_cont = st.text_input("Seu Nome")
                email_cont = st.text_input("Seu E-mail")
                assunto = st.selectbox("Assunto", ["Feedback", "Reclamação", "Sugestão", "Dúvida", "Outro"])
                mensagem = st.text_area("Mensagem:", height=150)
                
                if st.form_submit_button("📤 Enviar"):
                    if nome_cont and email_cont and mensagem:
                        EmailService.send_contact_form_notification(
                            nome_cont,
                            email_cont,
                            assunto,
                            mensagem
                        )
                        st.success("✅ Mensagem enviada! Responderemos em breve.")
                    else:
                        st.error("❌ Preencha todos os campos.")
        
        with sub_tab5:
            st.markdown(POLICIES['termos'])
            st.markdown(POLICIES['privacidade'])
            st.markdown(POLICIES['garantia'])
    
    # ========================================================================
    # TAB 4: ADMIN
    # ========================================================================
    with tab_admin:
        senha_admin = st.text_input("🔐 Senha Admin", type="password")
        if senha_admin == AppConfig.ADMIN_PASSWORD:
            st.success("✅ Acesso concedido")
            
            admin_tab1, admin_tab2, admin_tab3 = st.tabs(["📊 Dashboard", "👥 Usuários", "📋 Vendas"])
            
            with admin_tab1:
                col1, col2, col3, col4 = st.columns(4)
                users = db.get_all_users()
                orders = db.get_all_orders()
                
                with col1:
                    st.metric("👥 Usuários", len(users))
                with col2:
                    st.metric("📦 Pedidos Totais", len(orders))
                with col3:
                    total_revenue = sum(o['total'] for o in orders)
                    st.metric("💰 Receita Total", f"R$ {total_revenue:.2f}")
                with col4:
                    st.metric("⭐ Rating Médio", "4.8")
            
            with admin_tab2:
                st.write("### 👥 Usuários Cadastrados")
                if users:
                    df_users = pd.DataFrame([
                        {
                            'Email': u['email'],
                            'Nome': u['name'],
                            'Data': u['created_at'][:10]
                        }
                        for u in users
                    ])
                    st.dataframe(df_users, use_container_width=True)
                else:
                    st.info("Nenhum usuário cadastrado ainda.")
            
            with admin_tab3:
                st.write("### 📋 Últimas Vendas")
                if orders:
                    df_orders = pd.DataFrame([
                        {
                            'Pedido': o['order_number'],
                            'Cliente': o['email'],
                            'Total': f"R$ {o['total']:.2f}",
                            'Status': o['status'],
                            'Data': o['created_at'][:10]
                        }
                        for o in orders
                    ])
                    st.dataframe(df_orders, use_container_width=True)
                else:
                    st.info("Nenhum pedido registrado ainda.")
        
        elif senha_admin:
            st.error("❌ Senha incorreta")
        else:
            st.info("🔒 Digite a senha de administrador")
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.divider()
    st.markdown("""
    <div class="footer">
        <h3>🍪 MIRRA COOKIES</h3>
        <p>Premium Artisan Cookies | Qualidade Imperial</p>
        <div class="footer-links">
            <a class="footer-link" href="https://instagram.com/mirracookies">📷 Instagram</a>
            <a class="footer-link" href="https://facebook.com/mirracookies">👍 Facebook</a>
            <a class="footer-link" href="https://wa.me/5511999998888">💬 WhatsApp</a>
        </div>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 1rem 0;">
        <p style="font-size: 0.85rem;">© 2026 Mirra Cookies | Desenvolvido com ❤️</p>
        <p style="font-size: 0.75rem; margin-top: 1rem; opacity: 0.8;">Versão 1.0 | Todas as informações protegidas</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
