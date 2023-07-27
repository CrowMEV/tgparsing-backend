#!/usr/bin/env python3
import click
import uvicorn
from database.cli import db_group
from settings import config


@click.group()
def main_group():
    pass


@click.group("site")
def site_group():
    """Work with server"""


@site_group.command()
@click.option(
    "-h",
    "--host",
    default=config.HOST,
    help="IP address or local domain name to run server on",
)
@click.option("-p", "--port", default=config.PORT, help="Server port")
@click.option(
    "-l",
    "--log-level",
    default=config.DEBUG,
    help="Logging level. One of: [critical|error|warning|info|debug|trace]",
)
def run(
    host: str,
    port: int,
    log_level: str,
):
    """Run server"""
    app_name = "server:app"

    uvicorn.run(
        app_name, host=host, port=port, log_level=log_level, reload=True
    )


main_group.add_command(site_group)
main_group.add_command(db_group)


if __name__ == "__main__":
    main_group()
