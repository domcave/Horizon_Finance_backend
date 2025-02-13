"""cadd password



Revision ID: 57eb7baccb9b
Revises: 0718e6c41f31
Create Date: 2025-02-01 04:18:04.258518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57eb7baccb9b'
down_revision: Union[str, None] = '0718e6c41f31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###
