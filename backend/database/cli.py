import click


@click.group("db")
def db_group():
    """Work with db"""


@db_group.command()
@click.argument("path")
def load_roles(path: str):
    """Load roles to the "roles" table in the database"""
    import json

    from database.db_sync import db_sync
    from services.user.models import Role

    db = db_sync().__next__()
    path = "roles_data.json"
    with open(path) as file:
        data: dict = json.load(file)
    for key, value in data.items():
        role = Role(
            name=key,
            permissions=value,
        )
        db.add(role)
    db.commit()
