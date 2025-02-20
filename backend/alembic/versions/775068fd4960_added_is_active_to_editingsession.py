"""Added is_active to EditingSession

Revision ID: 775068fd4960
Revises: 98b11c48d65c
Create Date: 2025-02-14 20:31:42.188186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '775068fd4960'
down_revision: Union[str, None] = '98b11c48d65c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('editing_sessions', sa.Column('is_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('editing_sessions', 'is_active')
    # ### end Alembic commands ###
