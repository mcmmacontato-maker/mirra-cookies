# 🆘 Troubleshooting & FAQ - Mirra Cookies

## ❓ Perguntas Frequentes de Desenvolvimento

### 1. "Código de recuperação de senha não chega"

**Problema**: Clico em "Esqueci" mas não recebo o email.

**Solução**:
1. **Verifique a pasta de SPAM/Lixo** do seu email
2. **Certifique-se de configurar corretamente o `.env`**:
   ```env
   MIRRA_EMAIL=seu-email@gmail.com
   MIRRA_EMAIL_PASSWORD=xxxx xxxx xxxx xxxx  # 16 caracteres
   ```

3. **Para Gmail:**
   - Acesse: https://myaccount.google.com
   - Vá em: Segurança → Senhas de apps
   - Gere uma senha de app de 16 caracteres
   - Cole no `.env`

4. **Teste a conexão:**
   ```bash
   python test_everything.py
   ```

5. **Se continuar não funcionando:**
   - Ative modo DEBUG no `.env`: `DEBUG=True`
   - O código vai aparecer na tela durante reset

---

### 2. "Imagens dos cookies não aparecem"

**Problema**: Lugar do cookie vazio ou quebrado.

**Solução**:
- ✅ RESOLVIDO! Mudamos para Pexels que é mais confiável
- Se mesmo assim não carregar, há um placeholder automático
- Pode ser bloqueio do seu ISP/firewall
- Tente com VPN

**Se quiser adicionar suas próprias imagens:**
```python
# Edite config/settings.py
PRODUCT_IMAGES = {
    "c1": "sua-url-aqui",
}

# Ou use uma imagem local:
# 1. Coloque a imagem em uma pasta /static
# 2. Use: file:/static/seu-cookie.jpg
```

---

### 3. "Erro: 'no module named streamlit'"

**Problema**: `ModuleNotFoundError: No module named 'streamlit'`

**Solução**:
```bash
# Instale as dependências
pip install -r requirements.txt

# Ou manualmente
pip install streamlit pandas python-dotenv
```

---

### 4. "Banco de dados 'locked'"

**Problema**: `database is locked` ao fazer várias ações

**Solução**:
```bash
# SQLite pode ter arquivos de lock. Remova-os:
rm database/mirra_cookies.db-wal
rm database/mirra_cookies.db-shm

# Ou recrie o database (CUIDADO: perderá dados):
rm database/mirra_cookies.db
# Reinicie a app
```

---

### 5. "Senha muito fraca/comum"

**Problema**: Recebo erro mesmo com uma senha que achei boa.

**Solução**: A senha deve ter:
- ✅ Mínimo 8 caracteres
- ✅ Pelo menos 1 MAIÚSCULA
- ✅ Pelo menos 1 número
- ✅ Pelo menos 1 caractere especial: `!@#$%^&*()`
- ✅ Não ser um "top 20 das senhas comuns"

**Exemplos que funcionam:**
- `Mirra@2026!`
- `Cookie$Admin123`
- `Doce#Premium99`

---

### 6. "Admin login não funciona"

**Problema**: Digito a senha de admin mas não entra.

**Solução**:
1. Verifique a senha no `.env`:
   ```env
   ADMIN_PASSWORD=mirra_admin_2024  # padrão
   ```

2. Se editou, reinicie a app:
   ```bash
   # Pressione Ctrl+C no terminal
   # Depois execute novamente
   streamlit run app.py
   ```

3. Tente resetar para padrão:
   ```env
   ADMIN_PASSWORD=mirra_admin_2024
   ```

---

### 7. "Cupom não funciona"

**Problema**: Cupom válido mas diz "inválido".

**Solução**:

| Cupom | Requisito | Uso |
|-------|-----------|-----|
| MIRRA10 | Primeira compra | Apenas 1x |
| DOCE20 | Comprador recorrente | 1x a cada 30 dias |
| IMPERIAL30 | Comprador VIP | 1x a cada 30 dias |
| PREMIUM40 | Especial | 1x a cada 30 dias |

Se já usou há menos de 30 dias, precisa esperar.

---

### 8. "Streamlit app.py não inicia"

**Problema**: Erro ao executar `streamlit run app.py`

**Solução:**
```bash
# Verifique se está no diretório certo
cd /caminho/para/mirra-cookies

# Reinicie o ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Tente novamente
streamlit run app.py
```

---

### 9. "Erro ao criar conta"

**Problema**: Não consigo criar uma conta nova.

**Solução:**
- Email já existe? Use outro
- Email inválido? Use formato: `nome@dominio.com`
- Senha muito fraca? Adicione maiúscula, número, caractere especial
- Campos vazios? Preencha TODOS antes de enviar

---

### 10. "Pedido não é criado"

**Problema**: Clico em "FINALIZAR PEDIDO" mas nada acontece.

**Solução:**
1. **Verifique o endereço**: mínimo 10 caracteres
2. **Cartão de crédito**: 16 dígitos válidos (teste: `4111111111111111`)
3. **CVV**: 3 ou 4 dígitos
4. **Validade**: formato MM/AA (ex: 12/25)

**Teste rápido com cartão fictício:**
```
Número: 4111111111111111
Validade: 12/25
CVV: 123
```

---

## 🐛 Bugs Conhecidos Resolvidos

| Bug | Status | Solução |
|-----|--------|---------|
| Imagens não carregam | ✅ RESOLVIDO | URLs movidas para Pexels + fallback |
| Email não envia | ✅ RESOLVIDO | Implementado SMTP real |
| Dados perdidos ao reiniciar | ✅ RESOLVIDO | SQLite persistente |
| Senhas fracas aceitas | ✅ RESOLVIDO | Validação de força |
| Sem proteção força bruta | ✅ RESOLVIDO | Lockout após 5 tentativas |
| Sem auditoria | ✅ RESOLVIDO | Audit log completo |

---

## 🚀 Performance

### App lenta?

```bash
# 1. Limpe o cache do Streamlit
streamlit cache clear

# 2. Reduza tamanho do database
# Remova pedidos antigos do database

# 3. Verifique o computador
# RAM disponível? Processador ocupado?

# 4. Atualize dependências
pip install --upgrade streamlit pandas
```

---

## 🔐 Segurança

### ⚠️ NUNCA FAÇA ISSO:

```python
# ❌ ERRADO - Nunca hardcode secrets!
ADMIN_PASSWORD = "mirra_admin_2024"
MIRRA_EMAIL = "seu-email@gmail.com"

# ✅ CORRETO - Use variáveis de ambiente
import os
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
MIRRA_EMAIL = os.getenv("MIRRA_EMAIL")
```

```python
# ❌ ERRADO - Nunca comite .env
git add .env  # Não faça isso!

# ✅ CORRETO - Apenas exemplo
git add .env.example
```

```python
# ❌ ERRADO - Hash MD5/SHA1 é fraco
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ CORRETO - Use PBKDF2/bcrypt
password_hash = SecurityUtils.hash_password(password)
```

---

## 🧪 Testes

### Rodar todos os testes antes de deploy:
```bash
python test_everything.py
```

### Teste manual da app:
1. Crie uma conta teste
2. Recupere a senha
3. Adicione produtos ao carrinho
4. Aplique um cupom
5. Finalize um pedido
6. Verifique email de confirmação

---

## 📞 Suporte

Ainda com problemas? Verifique:

1. **Logs da aplicação**:
   ```bash
   # Terminal onde app está rodando
   # Observe mensagens de erro
   ```

2. **Console do navegador** (F12):
   - Aba "Console" para erros JavaScript
   - Aba "Network" para requisições

3. **Arquivo de teste**:
   ```bash
   python test_everything.py
   ```

4. **Documentação oficial**:
   - Streamlit: https://docs.streamlit.io
   - Python: https://docs.python.org
   - SQLite: https://www.sqlite.org/docs.html

---

## 💡 Dicas Úteis

### Desenvolvimento Rápido:
```bash
# Hot reload - mude arquivos e salve
# Streamlit recarrega automaticamente
```

### Debug:
```python
# Use st.write() para debugar
import streamlit as st
st.write("Debug value:", meu_valor)
st.json(meu_dict)  # Pretty print de JSON
```

### Performance Testing:
```bash
# Use --logger.level=debug para logs detalhados
streamlit run app.py --logger.level=debug
```

---

## 📈 Próximos Passos

Depois de resolver os problemas:

1. ✅ Teste localmente
2. ✅ Rode `test_everything.py`
3. ✅ Faça commit das mudanças
4. ✅ Deploy em Streamlit Cloud ou VPS
5. ✅ Configure domínio
6. ✅ Configure SSL/HTTPS
7. ✅ Faça backup do database
8. ✅ Monitore os logs

---

**Última atualização: Fevereiro de 2026**

*Precisa de ajuda? Abra uma issue ou entre em contato!*
