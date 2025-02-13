# Horizon_Finance_backend

Personal financial insights and guidance for those at different life stages.

**This has been deployed!!!** 

This backend provides various services to the Horizon Finance frontend.

# Starting Project — Local

_Assumes that Python and Postgres are installed_

run
`export FLASK_APP=run.py  `

then run
`flask run `

if you get an error that you python cant find flask_sqlalchemy restart the terminal and try again

# .env

In .env add:

1. DATABASE_URL
2. JWT_SECRET_KEY - for authentication
3. SECRET_KEY
4. PLAIN_CLIENT_ID
5. PLAID_SECRET_KEY
6. OPENAI_API_KEY
7. OPENAI_ASSISTANT_ID

# Postgresql

To create postgresql user run the following commands

```
psql -U postgres
CREATE ROLE financehorizon WITH LOGIN PASSWORD 'password'; #Creates user
ALTER ROLE financehorizon CREATEDB;
CREATE DATABASE "finance-horizon-db" OWNER financehorizon; #Creates DB
```

To connect to DB use

```
psql -U financehorizon -d finance-horizon-db
```

if it asks for password it's "password"

# Dependencies

Create Virtual Environment

```
python -m venv venv
source /venv/bin/activate
```

To install dependencies run

```
pip install requirements.txt
```

To save installed dependencies run

```
pip freeze > requirements.txt
```

# Browser testing

If you try to test flask directly in browser it might throw the following exception, ignore it.

```
127.0.0.1 - - [01/Feb/2025 03:03:57] "GET /favicon.ico HTTP/1.1" 404 -
```

# Alembic

To create migrations run

```
alembic revision --autogenerate -m "Message"
```

To run migrations run

```
alembic upgrade head
```
