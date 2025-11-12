# App


## 🤠 Possibilities:

- Home router (guest handles + secure handles)
- Feed (following + recomendation based on liked post)
- Full authentication, including sending an email for verification
- User and profile, + the ability to subscribe and view these subscriptions
- Posts, likes, and comments (create, edit, delete, statistics)
- Notification on create like, create comment like, create comment ando create subscribe
- Admin router (separate dependency for the superuser): statistics for the user, users, posts, subscriptions, etc., as well as dangerous actions directly related to deletion 
- Documentation from fastapi **/docs**

## Technologies:

- Python 3.12
- FastAPI
- Jinja 2
- SQLAlchemy
- Alembic
- PostgreSQL
- Poetry
- Docker


## Quick start

```
git clone https://github.com/vankaspr/yo-listen.git
cd yo-listen

# database & docker settings:
cp .env.example.docker .env.docker

cd src
cp .env.example .env

# install dependencies
poetry install

# run docker-compose
docker-compose up -d

# run
poetry run python -m main
```


