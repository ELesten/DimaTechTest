from sqlalchemy import text

from app.core.security import hash_password


def create_test_data(op):
    connection = op.get_bind()

    connection.execute(
        text("""
            INSERT INTO users (email, password, name, surname, is_admin) 
            VALUES (:email, :password, :name, :surname, :is_admin)
        """),
        {
            "email": "admin@example.com",
            "password": hash_password('admin'),
            "name": "admin",
            "surname": "admin",
            "is_admin": True
        }
    )


    connection.execute(
        text("""
            INSERT INTO users (email, password, name, surname, is_admin) 
            VALUES (:email, :password, :name, :surname, :is_admin)
        """),
        {
            "email": "user@example.com",
            "password": hash_password('user'),
            "name": "user",
            "surname": "user",
            "is_admin": False
        }
    )

    connection.execute(
        text("""
            INSERT INTO wallets (balance, user_id)
            VALUES (:balance, :user_id)
        """),
        {
            "balance": 0,
            "user_id": 2
        }
    )
