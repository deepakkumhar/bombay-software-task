# BOMBAY-SOFT

## Index

- [BOMBAY SOFT.](#bombay-soft)
  - [Index](#index)
    - [Introduction](#introduction)
    - [Installation](#installation)

### Introduction

- User authentication available(login and register)
- User update,change-password available
- User can see all register user
- Supports latest version of Python i.e. Python 3.10.3 along with Django 4.1.3 :zap:
- Api endpoind available on default server. :nail_care:

| Plugin   | **Version** |
| -------- | ----------- |
| pip      | 22.2.2      |
| Python   | 3.10.3      |
| Django   | 4.1.3       |
| Postgres | 11.6        |

### Installation

> ##### 1. Clone repository

```sh
git clone https://github.com/deepakkumhar/bombay-soft.git
```

> ##### 2. If you not having pip,Django let's install

```sh
sudo easy_install pip
```

> ##### 3. Create certual environment and activate

```sh
pipenv shell
```

> ##### 4. Setup The Project

```sh
pipenv install -r requirements.txt
```

> ##### 5. Create Database Manuanlly in PgAdmin

```sh
CREATE DATABASE <database_name>
```

> ##### 6. Setting up your database details and email config in .env

```sh
DB_NAME=DATABASE_NAME
DB_USER=DATABASE_USER
DB_PASSWORD=DATABASE_PASSWORD
DB_HOST=HOST_NAME
DB_PORT=PORT_NUMBER

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=xyz
EMAIL_HOST_USER=xyz@gmail.com
EMAIL_HOST_PASSWORD=xyz
RECIPIENT_ADDRESS=RecipientEmailAddress
```

> ##### 7. Create tables by Django migration

```sh
python manage.py makemigrations

python manage.py migrate
```

> ##### 8.All page available on @ `http://127.0.0.1:8000/`

```
Like Register user page - http://127.0.0.1:8000/register/

Like Login user page- http://127.0.0.1:8000/login/

Like User list page  - http://127.0.0.1:8000/user/

Like Update password page - http://127.0.0.1:8000/update-password/

Like Profile-edit page - http://127.0.0.1:8000/profile-edit/

Like logout user page - http://127.0.0.1:8000/logout/

```

> ##### 9. Extra functionality

- After user successful register email send on user
- Update password email send

<br />
