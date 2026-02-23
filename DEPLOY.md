# 🚀 Guia de Deploy - Mirra Cookies

## Opções de Deployment

### 1. **Streamlit Cloud** (Recomendado para começar)

**Vantagens:**
- Grátis até limite de uso
- Deploy em 1 clique
- HTTPS automático
- SSL grátis

**Passo a passo:**
1. Faça push do repo para GitHub
2. Acesse https://streamlit.io/cloud
3. Clique "New app"
4. Selecione seu repositório
5. Configure as variáveis de ambiente:
   - `MIRRA_EMAIL`
   - `MIRRA_EMAIL_PASSWORD`
   - `ADMIN_PASSWORD`
6. Deploy!

**Arquivo `secrets.toml` necessário:**
```toml
# .streamlit/secrets.toml (não commitar no Git)
MIRRA_EMAIL = "seu-email@gmail.com"
MIRRA_EMAIL_PASSWORD = "xxxx xxxx xxxx xxxx"
ADMIN_PASSWORD = "sua-senha-admin"
DEBUG = "False"
```

### 2. **Render (Alternativa barata)**

**Passo a passo:**
1. Crie conta em https://render.com
2. Novo "Web Service"
3. Conecte seu GitHub
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py`
5. Defina variáveis de ambiente
6. Deploy!

**Arquivo render.yaml:**
```yaml
services:
  - type: web
    name: mirra-cookies
    env: python
    pythonVersion: 3.11
    startCommand: streamlit run app.py --server.enableXsrfProtection=false
    envVars:
      - key: STREAMLIT_SERVER_HEADLESS
        value: true
      - key: STREAMLIT_SERVER_PORT
        value: 10000
```

### 3. **Heroku** (Descontinuado, não recomendado)

### 4. **VPS (AWS, DigitalOcean, Linode)**

**DigitalOcean - Droplet Básico ($4/mês):**

```bash
# SSH into your droplet
ssh root@seu_ip

# Update system
apt update && apt upgrade -y

# Install Python and pip
apt install python3 python3-pip python3-venv -y

# Clone repository
git clone https://github.com/seu-usuario/mirra-cookies.git
cd mirra-cookies

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (secure!)
nano .env
# Paste your config here

# Install supervisor para manter app rodando
apt install supervisor -y

# Create supervisor config
sudo nano /etc/supervisor/conf.d/mirra-cookies.conf
```

**Conteúdo do supervisor.conf:**
```ini
[program:mirra-cookies]
directory=/root/mirra-cookies
command=/root/mirra-cookies/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
autostart=true
autorestart=true
stderr_logfile=/var/log/mirra-cookies.err.log
stdout_logfile=/var/log/mirra-cookies.out.log
user=root
```

```bash
# Iniciar supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start mirra-cookies

# Configurar Nginx como reverse proxy
apt install nginx -y
sudo nano /etc/nginx/sites-available/default
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Restart Nginx
sudo nginx -s reload

# Add SSL com Let's Encrypt
apt install certbot python3-certbot-nginx -y
certbot --nginx -d seu-dominio.com
```

## ✅ Checklist Pré-Deploy

- [ ] Variáveis de ambiente configuradas
- [ ] `.env` criado localmente com dados reais
- [ ] Teste completo do sistema
- [ ] Email working (teste recuperar senha)
- [ ] Banco de dados criado
- [ ] Admin password alterado
- [ ] HTTPS habilitado
- [ ] Backup automático configurado
- [ ] Domínio apontando para servidor
- [ ] Monitoramento ativo

## 🔒 Segurança em Produção

### Essencial:
1. **HTTPS/SSL** ✅
2. **Environment variables** (não hardcode secrets)
3. **Database backups** automáticos
4. **Rate limiting** no Nginx
5. **Firewall** configurado
6. **Logs** monitorados
7. **Update** automático de dependências
8. **2FA** para admin

### Firewall (DigitalOcean):
```bash
# Allow SSH
ufw allow 22

# Allow HTTP/HTTPS
ufw allow 80
ufw allow 443

# Enable firewall
ufw enable

# Check status
ufw status
```

## 📈 Performance

### Otimizações:
1. Use CDN para imagens (Cloudflare)
2. Cache de página com Redis
3. Comprimir responses
4. Database indexes
5. Load balancing se necessário

### Monitorar:
```bash
# Check CPU/Memory
top

# Check disk space
df -h

# Check logs
tail -f /var/log/mirra-cookies.out.log
```

## 🔄 CI/CD (GitHub Actions)

**Arquivo: `.github/workflows/deploy.yml`**
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Render
        run: |
          curl https://api.render.com/deploy/srv-${{ secrets.RENDER_SERVICE_ID }}?key=${{ secrets.RENDER_API_KEY }}
```

## 📧 Email em Produção

### Gmail (Recomendado):
1. Use App Password (16 caracteres)
2. Enable 2FA na conta
3. Limite: 5 emails/segundo

### Alternativas:
- **SendGrid** (Gratuito: 100 emails/dia)
- **Mailgun** (Gratuito: 100 emails/dia)
- **AWS SES** (Muito barato, precisa verificar domain)
- **Brevo (Sendinblue)** (Gratuito: 300 emails/dia)

### Integração SendGrid:
```python
# Substitua EmailService por:
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to, subject, html_content):
    message = Mail(
        from_email='seu-email@mirracookies.com.br',
        to_emails=to,
        subject=subject,
        html_content=html_content
    )
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    return response.status_code == 202
```

## 💾 Backup

### Automático com cron:
```bash
# Backup diário do database
0 2 * * * cd /root/mirra-cookies && sqlite3 database/mirra_cookies.db ".backup 'database/backups/mirra_cookies_$(date +\%Y\%m\%d).db'"

# Upload para S3 (opcional)
0 3 * * * aws s3 cp /root/mirra-cookies/database/backups/ s3://seu-bucket/backups/ --recursive
```

## 🆘 Troubleshooting

### App não inicia?
```bash
# Check logs
sudo supervisorctl tail mirra-cookies stderr

# Restart
sudo supervisorctl restart mirra-cookies
```

### Email não envia?
```bash
# Test SMTP
python3 -c "
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('seu-email@gmail.com', 'seu-app-password')
print('✅ Conectado!')
"
```

### Database locked?
```bash
# SQLite locks
rm database/mirra_cookies.db-wal
rm database/mirra_cookies.db-shm
```

## 📞 Suporte

Em caso de problemas:
1. Verifique os logs
2. Teste localmente
3. Consulte documentação Streamlit
4. Abra issue no GitHub

---

**Última atualização: Fevereiro de 2026**
