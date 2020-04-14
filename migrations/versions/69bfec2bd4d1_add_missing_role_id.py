"""add-missing-role-id

Revision ID: 69bfec2bd4d1
Revises: f12b2945dfd5
Create Date: 2020-04-13 15:24:36.755450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69bfec2bd4d1'
down_revision = 'f12b2945dfd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('permission', sa.Column('role_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'permission', 'role', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'permission', type_='foreignkey')
    op.drop_column('permission', 'role_id')
    # ### end Alembic commands ###
