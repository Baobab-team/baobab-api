"""add-prefix-to-phone

Revision ID: 0e12206a33b6
Revises: 2371b9a06a06
Create Date: 2020-07-19 09:08:04.446824

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0e12206a33b6'
down_revision = '2371b9a06a06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('phone', sa.Column('prefix', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('phone', 'prefix')
    # ### end Alembic commands ###
