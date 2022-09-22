# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors
from config import host, user, password, dbname


# Creating tables if not exist
def tables_check():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS groups (
            group_id INT PRIMARY KEY,
            link VARCHAR (50) UNIQUE NOT NULL);""")

            print('Group Database is ready')

        with connection.cursor() as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY,
            username VARCHAR (40) NOT NULL,
            checkmark BOOLEAN NOT NULL);""")

            print('Users Database is ready')

    except Exception as _ex:
        print('Error while working with POSTGRESQL', _ex)

    finally:
        # noinspection PyUnboundLocalVariable
        if connection:
            # noinspection PyUnboundLocalVariable
            connection.close()


# Inserting groups into database
def groups_into_database(groups):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        connection.autocommit = True
        for group in groups:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO groups (link) VALUE ('{group}')"
                )

    except Exception as _ex:
        print('Error while working with POSTGRESQL', _ex)

    finally:
        # noinspection PyUnboundLocalVariable
        if connection:
            # noinspection PyUnboundLocalVariable
            connection.close()


# Retrieving groups from database
def groups_from_database() -> list:
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT group FROM groups"
            )
            lst = cursor.fetchall()
            return lst

    except Exception as _ex:
        print('Error while working with POSTGRESQL', _ex)

    finally:
        # noinspection PyUnboundLocalVariable
        if connection:
            # noinspection PyUnboundLocalVariable
            connection.close()


# Inserting user into database
def user_into_database(user_id, username) -> list:
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO users (user_id, username, checkmark) VALUES ('{user_id}', '{username}', FALSE)"
            )

        print(f"User with nickname {username} inserted successfully")

    except errors.lookup(UNIQUE_VIOLATION) as _ex:
        print(f"User with nickname {username} and id {user_id} already exists")

    except Exception as _ex:
        print('Error while working with POSTGRESQL', _ex)

    finally:
        # noinspection PyUnboundLocalVariable
        if connection:
            # noinspection PyUnboundLocalVariable
            connection.close()


# Returns checkmark of the user to see if message is sent or not
def check_mark(user_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT checkmark from users WHERE user_id = '{user_id}'"
            )
            return cursor.fetchone()

    except Exception as _ex:
        print('Error while working with POSTGRESQL', _ex)

    finally:
        # noinspection PyUnboundLocalVariable
        if connection:
            # noinspection PyUnboundLocalVariable
            connection.close()


# Sets checkmark about sent message to True
def message_sent_update(user_id):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET checkmark = TRUE WHERE user_id = {user_id}"
            )

    except Exception as _ex:
        print('Error while working with POSTGRESQL', _ex)

    finally:
        # noinspection PyUnboundLocalVariable
        if connection:
            # noinspection PyUnboundLocalVariable
            connection.close()


# Retrieving users from database
def users_from_database() -> list:
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM users"
            )
            lst = cursor.fetchall()
            return lst

    except Exception as _ex:
        print('Error while working with POSTGRESQL', _ex)

    finally:
        # noinspection PyUnboundLocalVariable
        if connection:
            # noinspection PyUnboundLocalVariable
            connection.close()


def amount_of_all_users():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT count(user_id) FROM users"
            )
            return cursor.fetchone()

    except Exception as _ex:
        print('Error while working with POSTGRESQL', _ex)

    finally:
        # noinspection PyUnboundLocalVariable
        if connection:
            # noinspection PyUnboundLocalVariable
            connection.close()


def amount_of_sent_users():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT count(user_id) FROM users WHERE checkmark = True"
            )
            return cursor.fetchone()

    except Exception as _ex:
        print('Error while working with POSTGRESQL', _ex)

    finally:
        # noinspection PyUnboundLocalVariable
        if connection:
            # noinspection PyUnboundLocalVariable
            connection.close()


def reset_checkmarks():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET checkmark = FALSE WHERE checkmark = TRUE"
            )

    except Exception as _ex:
        print('Error while working with POSTGRESQL', _ex)

    finally:
        # noinspection PyUnboundLocalVariable
        if connection:
            # noinspection PyUnboundLocalVariable
            connection.close()


def drop_table(table):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                f"DROP TABLE {table}"
            )

            print(f'Table {table} dropped')

    except Exception as _ex:
        print('Error while working with POSTGRESQL', _ex)

    finally:
        # noinspection PyUnboundLocalVariable
        if connection:
            # noinspection PyUnboundLocalVariable
            connection.close()
