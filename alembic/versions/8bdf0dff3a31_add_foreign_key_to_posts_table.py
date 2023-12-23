"""add foreign key to posts table

Revision ID: 8bdf0dff3a31
Revises: d53dd055c760
Create Date: 2023-12-23 16:36:36.210014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bdf0dff3a31'
down_revision: Union[str, None] = 'd53dd055c760'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fkey',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
