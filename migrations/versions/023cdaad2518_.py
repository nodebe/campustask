"""empty message

Revision ID: 023cdaad2518
Revises: e8fcf8dfae60
Create Date: 2021-08-23 09:40:29.388291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '023cdaad2518'
down_revision = 'e8fcf8dfae60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('bio', sa.Text(), nullable=True))
    op.add_column('task', sa.Column('facebook', sa.String(), nullable=True))
    op.add_column('task', sa.Column('website', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'website')
    op.drop_column('task', 'facebook')
    op.drop_column('task', 'bio')
    # ### end Alembic commands ###
