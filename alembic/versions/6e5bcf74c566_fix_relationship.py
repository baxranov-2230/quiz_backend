"""Fix relationship

Revision ID: 6e5bcf74c566
Revises: 20fe77edbae5
Create Date: 2025-03-05 16:40:58.296523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e5bcf74c566'
down_revision: Union[str, None] = '20fe77edbae5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('faculty_id', sa.Integer(), nullable=False))
    op.drop_constraint('groups_department_id_fkey', 'groups', type_='foreignkey')
    op.create_foreign_key(None, 'groups', 'faculties', ['faculty_id'], ['id'])
    op.drop_column('groups', 'department_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('department_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.create_foreign_key('groups_department_id_fkey', 'groups', 'departments', ['department_id'], ['id'])
    op.drop_column('groups', 'faculty_id')
    # ### end Alembic commands ###
