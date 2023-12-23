"""add content column to table

Revision ID: 184f0c2c3b48
Revises: 82af05a14b55
Create Date: 2023-12-23 15:48:05.417199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '184f0c2c3b48'
down_revision: Union[str, None] = '82af05a14b55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
