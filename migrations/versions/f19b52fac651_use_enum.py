""" use enum

Revision ID: f19b52fac651
Revises: df77c15e6a79
Create Date: 2020-02-18 20:16:08.833179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f19b52fac651'
down_revision = 'df77c15e6a79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('business_legal_name_key', 'business', type_='unique')
    op.drop_column('business', 'legal_name')
    op.alter_column('phone', 'type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('social_link', 'type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('social_link', 'type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('phone', 'type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('business', sa.Column('legal_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_unique_constraint('business_legal_name_key', 'business', ['legal_name'])
    # ### end Alembic commands ###
