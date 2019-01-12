"""empty message

Revision ID: 22f7cb359bd4
Revises: 662a8a465316
Create Date: 2019-01-12 16:11:36.625236

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '22f7cb359bd4'
down_revision = '662a8a465316'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('business', 'telephone')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('business', sa.Column('telephone', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
