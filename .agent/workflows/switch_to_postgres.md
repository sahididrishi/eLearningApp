---
description: Switch Django project from SQLite to PostgreSQL
---

# Switch to PostgreSQL

Follow these steps to migrate your Django project from SQLite to PostgreSQL.

## 1. Install PostgreSQL
Ensure PostgreSQL is installed and running on your system.
- **Mac (Homebrew)**: `brew install postgresql` then `brew services start postgresql`
- **Windows**: Download the installer from postgresql.org.

## 2. Install Python Adapter
You need `psycopg2` to allow Django to talk to PostgreSQL.

```bash
pip install psycopg2-binary
```

*Note: Add `psycopg2-binary` to your `requirements.txt` file.*

## 3. Create Database and User
Open your terminal and access the PostgreSQL shell:

```bash
psql postgres
```

Run the following SQL commands (change `myprojectuser` and `mypassword` to whatever you prefer):

```sql
CREATE DATABASE elearning_db;
CREATE USER myprojectuser WITH PASSWORD 'mypassword';
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE elearning_db TO myprojectuser;
\q
```

## 4. Update Django Settings
Open `elearning/settings.py` and modify the `DATABASES` section:

```python
# elearning/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'elearning_db',
        'USER': 'myprojectuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 5. Apply Migrations
Since this is a new database, you need to recreate the tables.

```bash
python manage.py migrate
```

## 6. Create Superuser
You will need a new admin account for this database.

```bash
python manage.py createsuperuser
```

## 7. Run Server
Start your server to verify everything works.

```bash
python manage.py runserver
```

> [!IMPORTANT]
> **Data Migration**: This process gives you a *fresh, empty* database. Your existing data (users, courses) in SQLite will NOT be automatically transferred. If you need to keep data, you would need to use `python manage.py dumpdata` (before switching) and `python manage.py loaddata` (after switching), but that can be complex with foreign keys. For development, starting fresh is usually easiest.
