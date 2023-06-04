import click

from database.db_sync import Session


@click.group("db")
def db_group():
    """Work with db"""


@db_group.command()
@click.argument("path")
def load_roles(path: str):
    """Load roles to the "roles" table in the database"""
    import json

    from services.role.models import Role

    with open(path) as file:
        data: dict = json.load(file)
    with Session() as session:
        for key, value in data.items():
            role = Role(
                name=key,
                permissions=value,
            )
            session.add(role)
        session.commit()


@db_group.command()
def add_admin():
    with Session() as session:
        import sys
        from passlib.context import CryptContext

        from pydantic import ValidationError
        from sqlalchemy import select
        from sqlalchemy.dialects.postgresql import insert

        from services.user.models import User
        from services.user.schemas import UserCreate

        firstname = input('Please, enter admin name: ')
        lastname = input('Please, enter admin surname: ')
        email = input('Please, enter admin email: ')

        stmt = select(User).where(User.email == email)
        user = session.execute(stmt).first()
        if user:
            sys.exit('There is such email in the database')
        password = input('Please enter admin password: ')
        prepared_data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": password
        }
        try:
            UserCreate(**prepared_data)
        except ValidationError as err:
            sys.exit(err)
        hashed_password = CryptContext(
            schemes=["bcrypt"], deprecated="auto"
        ).hash(password)
        prepared_data.pop('password')
        prepared_data.update(
            {
                "hashed_password": hashed_password,
                "is_superuser": True,
                "role_name": "admin"
            }
        )
        stmt = insert(User).values(**prepared_data)
        session.execute(stmt)
        session.commit()
        print('The admin was created successfully')
