Deployment & Development Notes
===============================

Quick notes for running in development and production.

Local (dev):

1. Install Python dependencies in a virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install Pillow
```

2. Run locally:

```bash
streamlit run app.py
```

Docker (recommended for production):

```bash
docker build -t mirra-cookies:latest .
docker run -p 8501:8501 mirra-cookies:latest
```

Or with docker-compose:

```bash
docker-compose up --build
```

Email configuration (Gmail)
---------------------------

If you plan to send real emails (password recovery, confirmations) configure environment variables for the container or your host. For Gmail use a Google App Password (2FA required).

1. Enable 2FA at https://myaccount.google.com/security
2. Generate App Password: https://myaccount.google.com/apppasswords (choose Mail / Other -> mirra-cookies)
3. Provide values to the container via environment variables or a `.env` file.

Example `docker-compose` snippet:

```yaml
services:
	web:
		image: mirra-cookies:latest
		environment:
			- MIRRA_EMAIL=seu-email@gmail.com
			- MIRRA_EMAIL_PASSWORD=xxxxxxxxxxxxxxxx
			- DEBUG=False
```

Never commit real credentials to version control. Use CI/CD secrets or a secret manager in production.

Image optimization:

- The repository includes `scripts/optimize_images.py` which uses Pillow to generate WebP optimized images.
- When building the Docker image the script runs during build if Pillow is available.
