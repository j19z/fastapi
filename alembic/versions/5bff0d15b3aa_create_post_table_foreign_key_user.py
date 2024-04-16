"""create post table foreign key user

Revision ID: 5bff0d15b3aa
Revises: 789646deaf66
Create Date: 2024-04-16 10:54:35.773198

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '5bff0d15b3aa'
down_revision: Union[str, None] = '789646deaf66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    pass
