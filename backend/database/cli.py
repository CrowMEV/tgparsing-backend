import click

from database.db_sync import Session


@click.group("db")
def db_group():
    """Work with db"""


@db_group.command()
@click.argument("path")
def load_roles(path: str, db_session=Session):
    """Load roles to the "roles" table in the database"""
    import json

    from services.role.models import Role

    with open(path) as file:
        data: dict = json.load(file)
    with db_session() as session:
        for item_data in data:
            role = Role(**item_data)
            session.add(role)
            session.commit()


@db_group.command()
@click.option("-f", "--firstname", help="User name", required=True)
@click.option("-l", "--lastname", help="User surname", required=True)
@click.option("-e", "--email", help="User email", required=True)
@click.option("-p", "--password", help="User password", required=True)
@click.option("-r", "--role", default="user", help="User role")
@click.option("-s", "--superuser", default=False, help="User is superuser")
def add_admin(firstname, lastname, email, password, role, superuser):
    with Session() as session:
        import sys
        from passlib.context import CryptContext

        from pydantic import ValidationError
        from sqlalchemy import select, and_
        from sqlalchemy.dialects.postgresql import insert

        from services.user.models import User
        from services.user.schemas import UserCreate

        stmt = select(User).where(and_(User.email == email))
        user = session.execute(stmt).first()
        if user:
            sys.exit("There is such email in the database")
        prepared_data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": password,
        }
        try:
            UserCreate(**prepared_data)
        except ValidationError as err:
            sys.exit(err)
        hashed_password = CryptContext(
            schemes=["bcrypt"], deprecated="auto"
        ).hash(password)
        prepared_data.pop("password")
        prepared_data.update(
            {
                "hashed_password": hashed_password,
                "is_superuser": superuser,
                "role_name": role,
            }
        )
        stmt = insert(User).values(**prepared_data)
        session.execute(stmt)
        session.commit()
        print("The admin was created successfully")
