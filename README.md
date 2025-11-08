# BARE MINIMUM FOR AUTH FASTAPI

## 📋 Opportunities:

- Register by username or email
- Login w/ access and refresh token's
- Jinja templates 
- Forgot & reset password 
- Oauth: github 
- User profile
- Admin section: statistics ando user-action

## 🛠️ Technologies used:

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Poetry 
- Docker


## 🚀 Quick start:

```
git clone https://github.com/vankaspr/bare-minimum-for-auth-app.git
cd bare-minimum-for-auth-app

# env file 
cp .env.docker.example .env.docker
cp .env.example .env

# install dependencies
poetry install 

# run 
poetry run python src/main.py

```