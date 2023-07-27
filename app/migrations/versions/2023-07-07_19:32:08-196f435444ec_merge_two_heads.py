"""merge two heads

Revision ID: 196f435444ec
Revises: 75b809694e2d, 8ae1b15678cd
Create Date: 2023-07-07 19:32:08.441779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '196f435444ec'
down_revision = ('75b809694e2d', '8ae1b15678cd')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
