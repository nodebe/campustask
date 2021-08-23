"""empty message

Revision ID: e8fcf8dfae60
Revises: eb3181501c12
Create Date: 2021-08-23 08:53:11.813865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8fcf8dfae60'
down_revision = 'eb3181501c12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('views', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'views')
    # ### end Alembic commands ###