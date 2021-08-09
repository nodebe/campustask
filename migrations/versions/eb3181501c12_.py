"""empty message

Revision ID: eb3181501c12
Revises: b40ea786ec23
Create Date: 2021-08-09 10:58:37.347493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb3181501c12'
down_revision = 'b40ea786ec23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('_image_name', sa.String(), nullable=True))
    op.drop_column('task', '_rating')
    op.drop_column('task', 'image_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('image_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('task', sa.Column('_rating', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('task', '_image_name')
    # ### end Alembic commands ###
