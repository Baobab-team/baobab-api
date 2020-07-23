"""update phone extension constraint

Revision ID: bcd90f88d077
Revises: 0e12206a33b6
Create Date: 2020-07-22 22:37:18.803466

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bcd90f88d077'
down_revision = '0e12206a33b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('phone', 'extension',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('phone', 'extension',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
