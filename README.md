# BARE MINIMUM FOR AUTH FASTAPI

## 📋 Opportunities:

- Register by username or email
- Login w/ access and refresh token's
- Jinja templates 
- Forgot & reset password 
- Oauth: github 
- User profile
- Admin section: statistics ando user-action (plus create superuser in code)
- Posts, likes and comments (create, update, delete) section

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
git clone https://github.com/vankaspr/yo-listen.git
cd yo-listen

# env file 
cp .env.docker.example .env.docker
cp .env.example .env

# install dependencies
poetry install 

# run 
cd src
poetry run python -m main

```