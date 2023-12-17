"""add table users

Revision ID: 5b6923a171f0
Revises: 16902bc585b2
Create Date: 2023-12-17 16:10:48.817790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b6923a171f0'
down_revision: Union[str, None] = '16902bc585b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=8),
               type_=sa.String(length=150),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=8),
               existing_nullable=False)
    # ### end Alembic commands ###
