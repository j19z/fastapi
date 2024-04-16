"""Create Posts Table

Revision ID: 789646deaf66
Revises: cada66dee293
Create Date: 2024-04-16 10:22:09.457993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '789646deaf66'
down_revision: Union[str, None] = 'cada66dee293'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa. Integer (), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean, server_default='True', nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
