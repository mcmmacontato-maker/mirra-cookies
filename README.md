# 🍪 MIRRA COOKIES - Premium Artisan Cookies

## ⚠️ ARQUIVO PRINCIPAL REORGANIZADO

Este arquivo antigo foi refatorado!

**A aplicação principal agora está em:**
- [`app.py`](app.py) - Aplicação Streamlit completa

## 📖 Documentação

- **[RESUMO.md](RESUMO.md)** - O que foi feito e como começar ⭐ **LEIA PRIMEIRO**
- **[README_NOVO.md](README_NOVO.md)** - Documentação técnica completa
- **[DEPLOY.md](DEPLOY.md)** - Guias de deployment
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - FAQ e solução de problemas

## 🚀 Quick Start

```bash
# 1. Instale dependências
pip install -r requirements.txt

# 2. Configure .env (importante!)
cp .env.example .env
# Edite .env com suas configurações de email

# 3. Teste tudo
python test_everything.py

# 4. Rode a app
streamlit run app.py
```

## ✅ Melhorias Implementadas

✅ **Imagens corrigidas** - URLs do Pexels + fallback automático
✅ **Email funcional** - SMTP real para recuperação de senha  
✅ **Banco persistente** - SQLite sem perda de dados
✅ **Segurança** - PBKDF2, validação, proteção força bruta
✅ **Refatorado** - Código modular e profissional
✅ **Documentado** - Guias completos para setup e deploy

## 📧 Configurar Email (IMPORTANTE!)

Para recuperação de senha funcionar, configure:

```env
MIRRA_EMAIL=seu-email@gmail.com
MIRRA_EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

Siga as instruções em [RESUMO.md](RESUMO.md#-como-começar)

## 📋 Estrutura do Projeto

```
mirra-cookies/
├── app.py                # ← Aplicação principal
├── requirements.txt     # Dependências
├── test_everything.py   # Testes
├── config/              # Configurações
├── database/            # SQLite
├── src/                 # Módulos
└── .env.example        # Variáveis de ambiente
```

## 🎯 Próximos Passos

1. Leia [RESUMO.md](RESUMO.md)
2. Configure o `.env` com seu email
3. Execute `python test_everything.py`
4. Rode `streamlit run app.py`
5. Teste a app localmente
6. Faça deploy com [DEPLOY.md](DEPLOY.md)

# --- FUNÇÕES DE SEGURANÇA E VALIDAÇÃO ---
def hash_password(password):
    """Hash de senha usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verifica se a senha corresponde ao hash"""
    return hash_password(password) == hashed

def validar_email(email):
    """Valida formato de email"""
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def simular_envio_email(email_destino, codigo):
    """Simula envio de código por email (em produção, usar serviço real como SendGrid/SES)"""
    st.session_state.recovery_email_sent = {
        "email": email_destino,
        "codigo": codigo,
        "timestamp": datetime.now().isoformat()
    }
    return True

# --- ESTADO DA SESSÃO ---
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'wishlist' not in st.session_state: st.session_state.wishlist = []
if 'users_db' not in st.session_state: 
    st.session_state.users_db = {
        "cliente@teste.com": {
            "senha_hash": hash_password("1234"),
            "nome": "Visitante Real",
            "email": "cliente@teste.com",
            "pedidos": 0,
            "ultimo_cupom_data": None,
            "criado_em": datetime.now().isoformat(),
            "historico_pedidos": []
        }
    }
if 'reviews_db' not in st.session_state: 
    st.session_state.reviews_db = {
        "c1": [{"usuario": "João Silva", "nota": 5, "texto": "Excelente! Muito crocante.", "data": "2026-02-15"}],
        "c2": [{"usuario": "Maria Santos", "nota": 5, "texto": "Delicioso, chegou rápido!", "data": "2026-02-18"}]
    }
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_email' not in st.session_state: st.session_state.user_email = ""
if 'desconto_aplicado' not in st.session_state: st.session_state.desconto_aplicado = 0.0
if 'recovery_code' not in st.session_state: st.session_state.recovery_code = None
if 'recovery_email_sent' not in st.session_state: st.session_state.recovery_email_sent = None
if 'page' not in st.session_state: st.session_state.page = "cardapio"

# --- CUPONS DISPONÍVEIS ---
CUPONS_RECORRENTES = {"DOCE20": 0.20, "IMPERIAL30": 0.30, "PREMIUM40": 0.40}
ADMIN_PASSWORD = "mirra_admin_2024"

# --- ESTILIZAÇÃO CSS PROFISSIONAL ---
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
    
    .social-icons {
        font-size: 1.5rem;
        margin-top: 1.5rem;
        letter-spacing: 1rem;
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
</style>
""", unsafe_allow_html=True)

# --- CARDÁPIO PREMIUM COMPLETO ---
PRODUCTS = {
    "c1": {
        "nome": "Ouro Belga", 
        "preco": 18.0, 
        "img": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=600&q=80",
        "desc": "Chocolate belga 54% cacau com massa amanteigada. Textura crocante perfeita.",
        "ingredientes": "Farinha, Manteiga, Chocolate Belga, Açúcar, Ovos",
        "alergênios": "Glúten, Leite, Ovos",
        "rating": 4.9
    },
    "c2": {
        "nome": "Veludo Rubro", 
        "preco": 20.0, 
        "img": "https://images.unsplash.com/photo-1590920591399-d1fa0b1ce37f?w=600&q=80",
        "desc": "Massa Red Velvet com recheio de cream cheese vanilla. Sabor único e sofisticado.",
        "ingredientes": "Farinha, Red Velvet, Cream Cheese, Baunilha",
        "alergênios": "Glúten, Leite, Ovos, Corante",
        "rating": 4.8
    },
    "c3": {
        "nome": "Pistache Imperial", 
        "preco": 24.0, 
        "img": "https://images.unsplash.com/photo-1585518419759-87cdde3bfb35?w=600&q=80",
        "desc": "Pistaches iranianos premium com chocolate branco. Exclusivo.",
        "ingredientes": "Farinha, Pistache Iraniano, Chocolate Branco",
        "alergênios": "Glúten, Leite, Amêndoa, Frutos Secos",
        "rating": 5.0
    },
    "c4": {
        "nome": "Double Dark Salt", 
        "preco": 19.0, 
        "img": "https://images.unsplash.com/photo-1499636138143-bd630f5cf446?w=600&q=80",
        "desc": "Cacau black, chocolate 70% com Flor de Sal. Intenso e equilibrado.",
        "ingredientes": "Farinha, Chocolate 70%, Cacau, Flor de Sal",
        "alergênios": "Glúten, Leite",
        "rating": 4.7
    },
    "c5": {
        "nome": "Brûlée Real", 
        "preco": 21.0, 
        "img": "https://images.unsplash.com/photo-1590080873967-85ac9a9ba3a1?w=600&q=80",
        "desc": "Massa de baunilha com casquinha de açúcar maçaricada. Sofisticado.",
        "ingredientes": "Farinha, Baunilha, Açúcar Cristal, Manteiga",
        "alergênios": "Glúten, Leite, Ovos",
        "rating": 4.9
    },
    "c6": {
        "nome": "Nutella Supreme", 
        "preco": 22.0, 
        "img": "https://images.unsplash.com/photo-1590080876486-0129de33d285?w=600&q=80",
        "desc": "Massa clássica recheada com Nutella pura. Irresistível.",
        "ingredientes": "Farinha, Nutella, Manteiga, Ovos",
        "alergênios": "Glúten, Leite, Ovos, Amêndoa",
        "rating": 4.6
    },
    "combo1": {
        "nome": "Combo Imperial (4 un)", 
        "preco": 70.0, 
        "img": "https://images.unsplash.com/photo-1585080876653-be1e43e8c3d0?w=600&q=80",
        "desc": "4 cookies premium à sua escolha com 15% de desconto especial.",
        "ingredientes": "Variado",
        "alergênios": "Consulte produto",
        "rating": 4.8
    },
}

# --- SIDEBAR COM LOGIN ---
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
                    if email_log in st.session_state.users_db:
                        user_rec = st.session_state.users_db[email_log]
                        if verify_password(senha_log, user_rec["senha_hash"]):
                            st.session_state.logged_in = True
                            st.session_state.user_email = email_log
                            st.success("✅ Login realizado!")
                            st.rerun()
                        else:
                            st.error("❌ Senha incorreta.")
                    else:
                        st.error("❌ E-mail não encontrado.")
            
            with col2:
                if st.button("🆘 Esqueci", use_container_width=True):
                    if email_log:
                        if not validar_email(email_log):
                            st.error("❌ E-mail inválido.")
                        elif email_log in st.session_state.users_db:
                            codigo_recuperacao = str(random.randint(100000, 999999))
                            st.session_state.recovery_code = codigo_recuperacao
                            simular_envio_email(email_log, codigo_recuperacao)
                            st.success("✅ Código enviado para seu e-mail!")
                            st.info(f"📧 Verifique: {email_log}")
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
                    elif len(nova_senha_reset) < 6:
                        st.error("❌ Mínimo 6 caracteres.")
                    else:
                        st.session_state.users_db[email_log]["senha_hash"] = hash_password(nova_senha_reset)
                        st.success("✅ Senha redefinida!")
                        st.session_state.recovery_code = None
                        st.rerun()

        with aba_auth[1]:
            st.write("**Crie sua conta:**")
            novo_nome = st.text_input("👤 Nome Completo", key="signup_name")
            novo_email = st.text_input("📧 E-mail", key="signup_email")
            nova_senha = st.text_input("🔐 Criar Senha", type="password", key="signup_pass")
            nova_senha_conf = st.text_input("🔐 Confirmar", type="password", key="signup_pass_conf")
            
            if st.button("✨ Criar Conta", use_container_width=True):
                if not novo_email or not nova_senha or not novo_nome:
                    st.error("❌ Preencha todos os campos.")
                elif not validar_email(novo_email):
                    st.error("❌ E-mail inválido!")
                elif novo_email in st.session_state.users_db:
                    st.error("❌ E-mail já cadastrado!")
                elif nova_senha != nova_senha_conf:
                    st.error("❌ Senhas não correspondem.")
                elif len(nova_senha) < 6:
                    st.error("❌ Mínimo 6 caracteres.")
                else:
                    st.session_state.users_db[novo_email] = {
                        "senha_hash": hash_password(nova_senha),
                        "nome": novo_nome,
                        "email": novo_email,
                        "pedidos": 0,
                        "ultimo_cupom_data": None,
                        "criado_em": datetime.now().isoformat(),
                        "historico_pedidos": []
                    }
                    st.success("✅ Conta criada!")
                    st.info("🎉 Bem-vindo! Faça login.")
    else:
        user_data = st.session_state.users_db[st.session_state.user_email]
        
        st.markdown(f"""
        <div class='about-box'>
            <h3>👑 {user_data['nome']}</h3>
            <p style='font-size: 0.9rem; color: #666;'>
            📧 {user_data['email']}<br>
            📦 {user_data['pedidos']} pedidos<br>
            📅 {user_data['criado_em'][:10]}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.cart = {}
            st.session_state.wishlist = []
            st.rerun()

# --- INTERFACE PRINCIPAL ---
st.markdown("<div class='header-title'>🍪 MIRRA COOKIES</div>", unsafe_allow_html=True)
st.markdown("<div class='tagline'>✨ Premium Artisan Cookies | Qualidade Imperial ✨</div>", unsafe_allow_html=True)

tab_menu, tab_cart, tab_pages, tab_admin = st.tabs(["🛍️ CARDÁPIO", "🛒 SACOLA", "ℹ️ MAIS", "🔐 ADMIN"])

with tab_menu:
    st.markdown("### 👨‍🍳 Nossas Especialidades")
    cols = st.columns(3)
    for i, (p_id, p) in enumerate(PRODUCTS.items()):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="product-card">
                    <img src="{p['img']}" class="product-image" alt="{p['nome']}">
                    <div class="product-name">{p['nome']}</div>
                    <div class="product-desc">{p['desc']}</div>
                    <div class="rating">⭐ {p['rating']}/5.0</div>
                    <div class="price-tag">R$ {p['preco']:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🛒 Adicionar", key=f"btn_{p_id}", use_container_width=True):
                    if p_id in st.session_state.cart:
                        st.session_state.cart[p_id]['qty'] += 1
                    else:
                        st.session_state.cart[p_id] = {**p, 'qty': 1}
                    st.toast(f"✅ {p['nome']} adicionado!")
            
            with col2:
                if st.button(f"❤️", key=f"wish_{p_id}", use_container_width=True):
                    if p_id not in st.session_state.wishlist:
                        st.session_state.wishlist.append(p_id)
                        st.toast("❤️ Favorito!")
                    else:
                        st.session_state.wishlist.remove(p_id)
                        st.toast("💔 Removido!")
            
            with st.expander(f"📋 {p['nome']}"):
                st.write(f"**Ingredientes:** {p['ingredientes']}")
                st.write(f"**Alergênios:** {p['alergênios']}")
                
                if p_id in st.session_state.reviews_db:
                    for rev in st.session_state.reviews_db[p_id]:
                        st.markdown(f"""
                        <div class="review-card">
                            <b>{rev['usuario']}</b> - {'⭐' * rev['nota']}<br>
                            {rev['texto']}<br>
                            <small>{rev['data']}</small>
                        </div>
                        """, unsafe_allow_html=True)
                
                if st.session_state.logged_in:
                    with st.form(f"review_{p_id}"):
                        nota_rev = st.slider("Sua nota:", 1, 5, 5, key=f"nota_{p_id}")
                        texto_rev = st.text_area("Comentário:", key=f"texto_{p_id}", height=80)
                        if st.form_submit_button("📤 Enviar"):
                            if p_id not in st.session_state.reviews_db:
                                st.session_state.reviews_db[p_id] = []
                            st.session_state.reviews_db[p_id].append({
                                "usuario": st.session_state.users_db[st.session_state.user_email]['nome'],
                                "nota": nota_rev,
                                "texto": texto_rev,
                                "data": datetime.now().strftime("%Y-%m-%d")
                            })
                            st.success("✅ Avaliação enviada!")

with tab_cart:
    if not st.session_state.logged_in:
        st.warning("⚠️ Faça login para ver a sacola.")
    elif not st.session_state.cart:
        st.info("🛒 Sacola vazia.")
    else:
        st.markdown("### 🛒 Seu Carrinho")
        
        total_bruto = 0
        for p_id, item in st.session_state.cart.items():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(f"**{item['nome']}**")
            with col2:
                qty = st.number_input(f"Qty", 1, 100, item['qty'], key=f"qty_{p_id}")
                st.session_state.cart[p_id]['qty'] = qty
            with col3:
                st.write(f"R$ {item['preco'] * qty:.2f}")
            with col4:
                if st.button("🗑️", key=f"del_{p_id}"):
                    del st.session_state.cart[p_id]
                    st.rerun()
            
            total_bruto += item['preco'] * item['qty']
        
        st.divider()
        
        user_info = st.session_state.users_db[st.session_state.user_email]
        
        with st.expander("🎟️ Cupom de Desconto"):
            cupom = st.text_input("Código:").upper()
            if st.button("✓ Validar", use_container_width=True):
                if user_info["pedidos"] == 0:
                    if cupom == "MIRRA10":
                        st.session_state.desconto_aplicado = total_bruto * 0.10
                        st.success("✅ 10% OFF - 1ª Compra!")
                    else:
                        st.error("❌ Use: MIRRA10")
                else:
                    if cupom == "MIRRA10":
                        st.error("❌ Apenas 1ª compra.")
                    elif cupom in CUPONS_RECORRENTES:
                        data_u = user_info["ultimo_cupom_data"]
                        if data_u is None:
                            dias = 999
                        else:
                            try:
                                data_anterior = datetime.fromisoformat(data_u)
                                dias = (datetime.now() - data_anterior).days
                            except:
                                dias = 999
                        
                        if dias >= 30 or data_u is None:
                            desconto = CUPONS_RECORRENTES[cupom]
                            st.session_state.desconto_aplicado = total_bruto * desconto
                            st.success(f"✅ {int(desconto*100)}% OFF!")
                        else:
                            st.warning(f"⏳ {30-dias} dias")
                    else:
                        st.error("❌ Inválido.")
        
        st.divider()
        
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

        with st.form("checkout"):
            st.write("### 📦 Entrega")
            nome_ent = st.text_input("Nome", value=user_info['nome'])
            end = st.text_area("Endereço completo")
            
            st.write("### 💳 Pagamento")
            metodo = st.selectbox("Método:", ["Pix", "Crédito", "Débito", "Dinheiro"])
            
            num_cartao = ""
            if metodo in ["Crédito", "Débito"]:
                num_cartao = st.text_input("Cartão (16 dígitos)", max_chars=16)
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input("Validade")
                with col2:
                    st.text_input("CVV", type="password")

            if st.form_submit_button("✅ FINALIZAR", use_container_width=True):
                if not end:
                    st.error("❌ Endereço obrigatório.")
                elif (metodo in ["Crédito", "Débito"]) and len(num_cartao) < 16:
                    st.error("❌ Cartão inválido.")
                else:
                    num_pedido = f"MRR-{random.randint(100000, 999999)}"
                    
                    pedido_info = {
                        "numero": num_pedido,
                        "data": datetime.now().isoformat(),
                        "itens": st.session_state.cart.copy(),
                        "total": total_final,
                        "endereco": end,
                        "pagamento": metodo,
                        "status": "Processando 🔄"
                    }
                    
                    user_info["historico_pedidos"].append(pedido_info)
                    user_info["pedidos"] += 1
                    
                    if st.session_state.desconto_aplicado > 0:
                        user_info["ultimo_cupom_data"] = datetime.now().isoformat()
                    
                    st.success("✅ Pedido finalizado!")
                    st.info(f"📦 **{num_pedido}**")
                    st.write(f"💚 R$ {total_final:.2f}")
                    st.write("📍 Seu pedido está sendo processado!")
                    
                    st.session_state.cart = {}
                    st.session_state.desconto_aplicado = 0.0

with tab_pages:
    sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5 = st.tabs(["📖 Sobre", "📋 Pedidos", "❓ FAQ", "📞 Contato", "📋 Políticas"])
    
    with sub_tab1:
        st.markdown("""
        <div class="about-box">
            <h2>🍪 Sobre Mirra Cookies</h2>
            <p>
            Empresa artesanal criada em 2022, dedicada a oferecer os melhores cookies premium do Brasil.
            Utilizamos apenas ingredientes de qualidade excepcional e técnicas artesanais.
            </p>
            <h3>✨ Nossa Missão</h3>
            <p>Criar experiências deliciosas com qualidade imperial.</p>
            <h3>🎯 Valores</h3>
            <ul>
            <li><b>Qualidade:</b> Melhores ingredientes</li>
            <li><b>Autenticidade:</b> Receitas caseiras</li>
            <li><b>Sustentabilidade:</b> Embalagens eco-friendly</li>
            <li><b>Satisfação:</b> 100% comprometido</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with sub_tab2:
        if st.session_state.logged_in:
            user_data = st.session_state.users_db[st.session_state.user_email]
            if user_data['historico_pedidos']:
                st.markdown("### 📦 Seus Pedidos")
                for pedido in reversed(user_data['historico_pedidos']):
                    data_pedido = datetime.fromisoformat(pedido['data']).strftime("%d/%m/%Y %H:%M")
                    st.markdown(f"""
                    <div class="order-card">
                        <b>{pedido['numero']}</b> - {data_pedido}<br>
                        <span class="status-badge status-{pedido['status'].split()[0].lower()}">
                            {pedido['status']}
                        </span><br>
                        <b>R$ {pedido['total']:.2f}</b> | 📍 {pedido['endereco'][:40]}...
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander(f"Ver itens - {pedido['numero']}"):
                        for p_id, item in pedido['itens'].items():
                            st.write(f"• {item['nome']} x{item.get('qty', 1)} - R$ {item['preco'] * item.get('qty', 1):.2f}")
            else:
                st.info("📭 Nenhum pedido ainda.")
        else:
            st.warning("Faça login para ver seus pedidos.")
    
    with sub_tab3:
        st.markdown("## ❓ FAQ")
        faqs = [
            ("Quanto tempo dura?", "7 dias em ambiente fresco. Consumir em até 3 dias."),
            ("Fazem delivery?", "Sim! 24-48h na região metropolitana."),
            ("Posso devolver?", "Garantia de 7 dias. Sem perguntas."),
            ("Cookies personalizados?", "Sim! Mínimo 10 dias de antecedência."),
            ("Como armazenar?", "Fresco, seco, longe de umidade. Nunca refrigere!"),
            ("Cupons combinam?", "Não. Um cupom por pedido."),
        ]
        for pergunta, resposta in faqs:
            with st.expander(f"**{pergunta}**"):
                st.write(resposta)
    
    with sub_tab4:
        st.markdown("## 📞 Contato")
        st.markdown("""
        <div class="about-box">
            <p><b>📍 Endereço:</b> Rua Imperial, 123 - São Paulo, SP</p>
            <p><b>📧 E-mail:</b> contato@mirracookies.com.br</p>
            <p><b>📱 WhatsApp:</b> (11) 99999-8888</p>
            <p><b>🕐 Horário:</b><br>
            Seg-Sex: 9h-18h | Sáb: 10h-14h | Dom: Fechado
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("contact_form"):
            nome_cont = st.text_input("Seu Nome")
            email_cont = st.text_input("Seu E-mail")
            assunto = st.selectbox("Assunto", ["Feedback", "Reclamação", "Sugestão", "Outro"])
            mensagem = st.text_area("Mensagem:", height=150)
            
            if st.form_submit_button("📤 Enviar"):
                if nome_cont and email_cont and mensagem:
                    st.success("✅ Mensagem enviada!")
                else:
                    st.error("❌ Preencha tudo.")
    
    with sub_tab4:
        st.markdown("""
        <div class="about-box">
            <h3>📋 Termos</h3>
            <p><b>Entrega:</b> Até 48h úteis.</p>
            <p><b>Devolução:</b> 7 dias para defeitos.</p>
            <p><b>Alergênios:</b> Consulte sempre os ingredientes.</p>
            <p><b>Privacidade:</b> Dados não compartilhados.</p>
            <p><b>Garantia:</b> 100% qualidade garantida.</p>
        </div>
        """, unsafe_allow_html=True)

with tab_admin:
    senha_admin = st.text_input("🔐 Admin", type="password")
    if senha_admin == ADMIN_PASSWORD:
        st.success("✅ Acesso concedido")
        
        admin_tab1, admin_tab2, admin_tab3 = st.tabs(["📊 Dashboard", "👥 Usuários", "🛍️ Vendas"])
        
        with admin_tab1:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("👥 Usuários", len(st.session_state.users_db))
            with col2:
                pedidos_totais = sum(u['pedidos'] for u in st.session_state.users_db.values())
                st.metric("📦 Pedidos", pedidos_totais)
            with col3:
                st.metric("🍪 Avaliadas", len(st.session_state.reviews_db))
            with col4:
                st.metric("⭐ Média", "4.8")
        
        with admin_tab2:
            st.write("### 👥 Usuários")
            df_users = pd.DataFrame(st.session_state.users_db).T[['nome', 'email', 'pedidos', 'criado_em']]
            st.dataframe(df_users, use_container_width=True)
        
        with admin_tab3:
            st.write("### 🛍️ Vendas")
            produto_sales = {p['nome']: random.randint(5, 50) for p in PRODUCTS.values()}
            st.bar_chart(produto_sales)
    
    elif senha_admin:
        st.error("❌ Senha incorreta")
    else:
        st.info("🔒 Admin")

# --- RODAPÉ ---
st.divider()
st.markdown("""
<div class="footer">
    <h3>🍪 MIRRA COOKIES</h3>
    <p>Premium Artisan Cookies | Qualidade Imperial</p>
    <div class="social-icons">📘 🎥 🐦 📷</div>
    <hr style="border-color: rgba(255,255,255,0.1); margin: 1rem 0;">
    <p style="font-size: 0.85rem;">© 2026 Mirra Cookies | Desenvolvido com ❤️</p>
</div>
""", unsafe_allow_html=True)
