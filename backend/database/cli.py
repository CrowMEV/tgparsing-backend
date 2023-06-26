import json
import sys

import click
from pydantic import ValidationError
from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert

from database.db_sync import Session
from services.role.models import Role
from services.user.models import User
from services.user.schemas import UserCreate
from services.user.utils.security import get_hash_password


@click.group("db")
def db_group():
    """Work with db"""


@db_group.command()
@click.argument("path")
def load_roles(path: str, db_session=Session):
    """Load roles to the "roles" table in the database"""

    with open(path) as file:
        data: dict = json.load(file)
    with db_session() as session:
        for item_data in data:
            stmt = insert(Role).values(**item_data).on_conflict_do_nothing()
            session.execute(stmt)
            session.commit()


@db_group.command()
@click.option("-f", "--firstname", help="User name", required=True)
@click.option("-l", "--lastname", help="User surname", required=True)
@click.option("-e", "--email", help="User email", required=True)
@click.option("-p", "--password", help="User password", required=True)
@click.option("-r", "--role", default="user", help="User role")
@click.option("-s", "--superuser", default=False, help="User is superuser")
def add_admin(
    firstname: str,
    lastname: str,
    email: str,
    password: str,
    role: str,
    superuser: str,
):
    with Session() as session:
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
            UserCreate.parse_obj(prepared_data)
        except ValidationError as err:
            sys.exit(str(err))
        hashed_password = get_hash_password(password)
        prepared_data.pop("password")
        prepared_data.update(
            {
                "hashed_password": hashed_password,
                "is_superuser": superuser,
                "role_name": role.upper(),
            }
        )
        stmt = insert(User).values(**prepared_data)
        session.execute(stmt)
        session.commit()
        print("The admin was created successfully")
