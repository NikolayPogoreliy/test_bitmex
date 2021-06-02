# BITMEX gateway

## Setup

### 1.Clone project

`git clone https://github.com/NikolayPogoreliy/test_bitmex.git`

#### or

`git clone git@github.com:NikolayPogoreliy/test_bitmex.git`

### 2.Install packages

`pip install -r requirements.txt`

### 3.Install and configure DB

`sudo apt install postgresql postgresql-contrib`

`psql postgres`

`CREATE DATABASE <DB_NAME>;`

`\connect <DB_NAME>`

`CREATE EXTENSION pgcrypto;`

`CREATE USER <DB_USER> WITH PASSWORD '<DB_PASSWORD>';`

`GRANT ALL PRIVILEGES ON <DB_NAME> TO <DB_USER>;`

### 4 Configure an application

#### 4.1 Create .env-file

Copy file `.env-example` to `.env` and edit it

PGCRYPTO_KEY=<PG_CRYPTO_KEY>

DB_NAME=<DB_NAME>

DB_USER=<DB_USER>

DB_PASSWORD=<DB_PASSWORD>

DB_HOST=<DB_HOST>

DB_PORT=<DB_PORT>

CHANNELS_HOST=127.0.0.1

CHANNELS_PORT=6379

BITBEX_FEED_PERIOD=5.0

DEBUG=True

#### 4.2 Run migrations

`./manage.py migrate`

#### 4.3 Create superuser

`./manage.py createsuperuser`

#### 4.4 Load fixtures

`./manage.py loaddata fixtures/account_fixture.json`

### 5 Start application

`./manage.py runserver`

`./manage.py runws`
