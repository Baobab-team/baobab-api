"""add-address-raw-field

Revision ID: 97f4100034cf
Revises: bcd90f88d077
Create Date: 2020-08-15 15:43:58.077706

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '97f4100034cf'
down_revision = 'bcd90f88d077'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('business', sa.Column('address_raw', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('business', 'address_raw')
    # ### end Alembic commands ###