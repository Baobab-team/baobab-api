"""empty message

Revision ID: 9c172910aa5d
Revises: 
Create Date: 2020-06-04 22:15:49.936039

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c172910aa5d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('business',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('slogan', sa.String(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('accepted_at', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.String(), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.Column('payment_types', sqlalchemy_utils.types.scalar_list.ScalarListType(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start', sa.Time(), nullable=False),
    sa.Column('end', sa.Time(), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('street_number', sa.String(), nullable=True),
    sa.Column('street_type', sa.String(length=5), nullable=True),
    sa.Column('street_name', sa.String(), nullable=True),
    sa.Column('direction', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('zip_code', sa.String(), nullable=True),
    sa.Column('province', sa.String(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('business_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('business_hour',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day', sa.String(), nullable=False),
    sa.Column('closing_time', sa.Time(), nullable=False),
    sa.Column('opening_time', sa.Time(), nullable=False),
    sa.Column('business_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phone',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.Column('extension', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('business_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('social_link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('business_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('business_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'business_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    op.drop_table('social_link')
    op.drop_table('plate')
    op.drop_table('phone')
    op.drop_table('business_hour')
    op.drop_table('address')
    op.drop_table('menu')
    op.drop_table('business')
    op.drop_table('tag')
    op.drop_table('restaurant')
    op.drop_table('category')
    # ### end Alembic commands ###