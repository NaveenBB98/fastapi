"""create users table

Revision ID: d53dd055c760
Revises: 184f0c2c3b48
Create Date: 2023-12-23 15:56:40.457485

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd53dd055c760'
down_revision: Union[str, None] = '184f0c2c3b48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer(),nullable=False),sa.Column('email',sa.String(),nullable=False),sa.Column('password',sa.String(),nullable=False),sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
