"""init

Revision ID: 406b38d5b565
Revises: 
Create Date: 2023-10-11 01:11:49.202277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '406b38d5b565'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('login', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('date_registration', sa.DATE)
    )


def downgrade() -> None:
    op.drop_table('users')
