# Local PostgreSQL Setup Guide for Elorah Jewelry

This guide walks you through setting up the local PostgreSQL database for the Elorah Jewelry Django project. It includes solutions for common errors you might encounter when using pgAdmin.

## Prerequisites
1. You must have **PostgreSQL 16** (or newer) installed on your system.
2. You must have **pgAdmin 4** installed (usually comes bundled with the PostgreSQL installer on Windows).

---

## Step 1: Open pgAdmin and Connect
1. Open **pgAdmin 4** on your computer.
2. In the left sidebar, expand **Servers** and click on your PostgreSQL 16 server. You will be prompted to enter your master password.
3. Expand **Databases**, right-click on the default **postgres** database, and select **Query Tool**.

---

## Step 2: Create the Database
*(Note: pgAdmin tries to group queries into a single "transaction", which causes the error CREATE DATABASE cannot run inside a transaction block. To fix this, we run the database creation step completely by itself).*

1. In the Query Tool, paste the following command:
   ``sql
   CREATE DATABASE elorah_jewelry;
   ``
2. Click the **Execute/Play** button (▶️).
3. Wait for the message: Query returned successfully.

---

## Step 3: Refresh the UI to See the Database
pgAdmin does not automatically show newly created databases.
1. Right-click on the folder icon that says **Databases** in the left sidebar.
2. Click **Refresh**.
3. You should now see elorah_jewelry listed under the databases.

---

## Step 4: Create the User and Grant Permissions
Now we need to create the elorah_user, set their password, and give them ownership of the new database.

1. In the left sidebar, right-click on your newly created **elorah_jewelry** database and select **Query Tool**. (It is crucial that you open the Query Tool *inside* the new database, not the old postgres one).
2. Delete any old text in the Query Tool, paste the following block of code, and click **Execute/Play** (▶️):

   ``sql
   CREATE USER elorah_user WITH PASSWORD 'pass';
   ALTER ROLE elorah_user SET client_encoding TO 'utf8';
   ALTER ROLE elorah_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE elorah_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE elorah_jewelry TO elorah_user;
   ``

---

## Step 5: Fix the "Public Schema" Permission Error
In PostgreSQL 15 and newer, the default "public" schema is locked down for security. If you skip this step, Django will crash with the error: psycopg.errors.InsufficientPrivilege: permission denied for schema public.

1. Still inside the Query Tool for the **elorah_jewelry** database, delete the previous text.
2. Paste this single command and click **Execute/Play** (▶️):
   ``sql
   GRANT ALL ON SCHEMA public TO elorah_user;
   ``

---

## Step 6: Connect Django to the Database
Now that the database is fully configured and secured, return to your code editor (e.g., VS Code).

1. Ensure your .env file at the root of the project contains the correct connection URL. It should look like this:
   ``env
   DATABASE_URL=postgres://elorah_user:pass@localhost:5432/elorah_jewelry
   ``
   *(Note: If your PostgreSQL installed on port 5433 instead of the default 5432, simply change the number in the URL above).*

2. Open your VS Code terminal (ensure your virtual environment is activated) and run the migrations to create the tables:
   ``bash
   py manage.py migrate
   ``

3. Create your admin account:
   ``bash
   py manage.py createsuperuser
   ``

4. Start the server!
   ``bash
   py manage.py runserver
   ``
