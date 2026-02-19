# 🍪 Mirra Cookies - Premium Artisan Cookies E-commerce

## ✨ Sobre o Projeto

Mirra Cookies é uma aplicação **web full-stack** para e-commerce de cookies premium artesanais. Desenvolvida com **Streamlit**, oferece:

- ✅ Autenticação segura com validação de força de senha
- ✅ Sistema de recuperação de senha via **email real** (Gmail/Outlook)
- ✅ Banco de dados **SQLite persistente**
- ✅ Carrinho de compras com cupons de desconto
- ✅ Histórico de pedidos
- ✅ Sistema de avaliações de produtos
- ✅ Painel administrativo
- ✅ Envio de emails de confirmação
- ✅ Proteção contra ataques comuns
- ✅ Auditoria de ações

## 🚀 Recursos Implementados

### 1. **Sistema de Autenticação Melhorado**
- ✅ Criptografia de senha com PBKDF2 (em vez de SHA-256 simples)
- ✅ Validação de força de senha
- ✅ Proteção contra força bruta (5 tentativas = bloqueio de 15 min)
- ✅ Logout com limpeza de sessão

### 2. **Recuperação de Senha Funcional**
- ✅ Envio de código **via email real** (Gmail, Outlook, etc)
- ✅ Código expira em 15 minutos
- ✅ Validação de código antes de redefinir senha
- ✅ Log de auditoria

### 3. **Banco de Dados Persistente**
- ✅ SQLite com schema completo
- ✅ Tabelas: usuarios, pedidos, avaliações, recuperação, auditoria
- ✅ Sem perda de dados ao reiniciar a aplicação

### 4. **Imagens de Produtos**
- ✅ URLs de imagens atualizadas (Pexels em vez de Unsplash)
- ✅ Fallback automático para placeholder se imagem não carregar
- ✅ Otimizadas para web

### 5. **Segurança Melhorada**
- ✅ Validação de entrada (XSS protection)
- ✅ Validação de cartão de crédito (Luhn Algorithm)
- ✅ Masking de dados sensíveis
- ✅ Audit log de todas as ações importantes
- ✅ Proteção contra senhas comuns

### 6. **Email Service**
- ✅ Recuperação de senha com templates HTML
- ✅ Confirmação de pedido
- ✅ Notificação de contato para admin
- ✅ Suporte a Gmail e Outlook SMTP

## ⚙️ Setup e Instalação

### Pré-requisitos
- Python 3.8+
- pip ou conda
- Conta Gmail/Outlook (para envio de emails)

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/mirra-cookies.git
cd mirra-cookies
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

**IMPORTANTE: Setup de Email para Recuperação de Senha**

#### Option 1: Gmail (Recomendado)
1. Acesse: https://myaccount.google.com/apppasswords
2. Selecione "Mail" e "Windows Computer"
3. Copie a senha gerada de 16 caracteres
4. Crie arquivo `.env` na raiz do projeto:

```env
MIRRA_EMAIL=seu-email@gmail.com
MIRRA_EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
DEBUG=False
ADMIN_PASSWORD=mirra_admin_2024
```

#### Option 2: Outlook
```env
MIRRA_EMAIL=seu-email@outlook.com
MIRRA_EMAIL_PASSWORD=sua-senha-outlook
DEBUG=False
```

### 5. Rodando a aplicação
```bash
streamlit run app.py
```

A aplicação abrirá em: `http://localhost:8501`

## 📱 Usando a Aplicação

### Para Clientes
1. **Criar Conta**: Use a aba "Cadastro" com:
   - Nome completo
   - Email válido
   - Senha forte (8+ caracteres, maiúscula, número, especial)

2. **Login**: Acesse sua conta com email e senha

3. **Recuperar Senha**: Clique em "Esqueci"
   - Digite seu email
   - Receba código no seu email
   - Insira o código e nova senha

4. **Comprar**:
   - Adicione produtos à sacola
   - Aplique cupom (MIRRA10 para primeira compra)
   - Finalize o pedido
   - Receba confirmação por email

### Para Administrador
- Clique na aba "🔐 ADMIN"
- Digite a senha (padrão: `mirra_admin_2024`)
- Veja dashboard com:
  - Total de usuários
  - Número de pedidos
  - Receita total
  - Lista de usuários e pedidos

## 🎟️ Cupons Disponíveis

| Cupom | Desconto | Requisito | Frequência |
|-------|----------|-----------|------------|
| MIRRA10 | 10% | Primeira compra | Uma vez |
| DOCE20 | 20% | Comprador recorrente | A cada 30 dias |
| IMPERIAL30 | 30% | Comprador VIP | A cada 30 dias |
| PREMIUM40 | 40% | Cupom especial | A cada 30 dias |

## 📧 Configuração de Email - Troubleshooting

### Gmail não envia código?
- ✅ Verifique se 2FA está ativado
- ✅ Use "App Password" (16 caracteres), não sua senha normal
- ✅ Verifique a variável `MIRRA_EMAIL_PASSWORD` no `.env`

### Outlook não funciona?
- ✅ Use sua senha real (não app password)
- ✅ Verifique se a conta permite acesso de apps menos seguros

### Teste rápido
```python
from src.email_service import EmailService
EmailService.send_recovery_code("seu-email@gmail.com", "123456", "Teste")
```

## 🗄️ Estrutura do Projeto

```
mirra-cookies/
├── app.py                    # Aplicação principal Streamlit
├── requirements.txt          # Dependências
├── .env.example             # Exemplo de configuração
├── .gitignore              # Git ignore
│
├── config/
│   └── settings.py         # Configurações centralizadas
│
├── database/
│   └── db.py              # Gerenciador do banco de dados SQLite
│
├── src/
│   ├── email_service.py    # Serviço de envio de emails
│   ├── security.py         # Funções de segurança e validação
│   └── products.py         # Catálogo de produtos
│
└── database/
    └── mirra_cookies.db    # Banco de dados (criado automaticamente)
```

## 🔒 Segurança

### Implementado:
- ✅ Senhas hasheadas com PBKDF2
- ✅ Validação de força de senha
- ✅ Proteção contra força bruta
- ✅ Validação de cartão de crédito (Luhn)
- ✅ Sanitização de entrada
- ✅ HTTPS recomendado para produção
- ✅ Audit log de ações
- ✅ Deteccção de senhas comuns

### Recomendações para Produção:
1. Usar HTTPS/SSL
2. Mover `.env` para variáveis de ambiente do servidor
3. Implementar rate limiting
4. Configurar CORS properly
5. Usar provider de pagamento real (Stripe, MercadoPago)
6. Implementar 2FA para admin
7. Backup automático do banco de dados
8. Monitorar audit logs

## 💳 Pagamento

Atualmente, a aplicação aceita os seguintes métodos:
- PIX (manual)
- Cartão de Crédito (validação básica, requer integração real)
- Cartão de Débito (validação básica, requer integração real)
- Dinheiro (reembolso na entrega)

**Para Produção**: Integrar com Stripe, MercadoPago ou PagSeguro

## 🧪 Testando Localmente

### Usuário de Teste (removido - use cadastro normal)
```
Email: cliente@teste.com
Senha: Teste@123
```

### Conta Admin
```
Senha: mirra_admin_2024
Mudé em .env para ADMIN_PASSWORD=sua_senha
```

## 📊 Estatísticas

| Métrica | Valor |
|---------|-------|
| Produtos | 7 cookies premium |
| Avaliação média | 4.8/5.0 ⭐ |
| Métodos de pagamento | 4 |
| Cupons ativos | 4 |
| Segurança | ✅ PBKDF2, Validação, Audit |

## 🐛 Bugs Corrigidos

1. ✅ **Imagens não carregavam**: URLs do Unsplash fora do ar → Pexels com fallback
2. ✅ **Email de recuperação não funcionava**: Função simulava → Implementado SMTP real
3. ✅ **Dados perdidos ao reiniciar**: Session state volátil → SQLite persistente
4. ✅ **Senhas fracas**: SHA-256 simples → PBKDF2 + validação
5. ✅ **Sem proteção contra força bruta**: Nenhuma → Lockout após 5 tentativas
6. ✅ **Falta de auditoria**: Sem logs → Audit log completo

## 🚀 Próximas Melhorias (Roadmap)

- [ ] Autenticação social (Google, Facebook)
- [ ] Integração com Stripe/MercadoPago
- [ ] Notificação em tempo real via WebSocket
- [ ] Sistema de cupons dinâmicos para admin
- [ ] Email marketing automático
- [ ] App mobile (React Native)
- [ ] Dashboard de análise avançado
- [ ] Sistema de afiliados
- [ ] Cashback program
- [ ] Integração com WhatsApp Business API

## 📄 Licença

MIT License - veja LICENSE.md

## 👨‍💻 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Contato

- 📧 Email: contato@mirracookies.com.br
- 📱 WhatsApp: (11) 99999-8888
- 📷 Instagram: @mirracookies
- 👍 Facebook: mirracookiesoficial

## 🙏 Agradecimentos

- Streamlit pela plataforma excelente
- Pexels pelas imagens gratuitas
- Comunidade Python

---

**Made with ❤️ by Mirra Cookies Team**

*Última atualização: Fevereiro de 2026*
