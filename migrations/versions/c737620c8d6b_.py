"""empty message

Revision ID: c737620c8d6b
Revises: 1d918079e131
Create Date: 2019-09-17 17:18:36.401328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c737620c8d6b'
down_revision = '1d918079e131'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('img_url', sa.String(length=200), nullable=False),
    sa.Column('link_to', sa.String(length=200), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('banner')
    # ### end Alembic commands ###