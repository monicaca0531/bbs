"""empty message

Revision ID: e4a77cd4fb94
Revises: c737620c8d6b
Create Date: 2019-09-17 17:22:10.202158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4a77cd4fb94'
down_revision = 'c737620c8d6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('banner', sa.Column('name', sa.String(length=200), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('banner', 'name')
    # ### end Alembic commands ###