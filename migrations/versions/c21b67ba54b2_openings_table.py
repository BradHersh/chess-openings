"""openings table

Revision ID: c21b67ba54b2
Revises: 5acd98042a65
Create Date: 2021-05-07 16:28:48.615362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c21b67ba54b2'
down_revision = '5acd98042a65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('openings')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('openings',
    sa.Column('name', sa.VARCHAR(length=140), nullable=False),
    sa.Column('FEN', sa.VARCHAR(length=140), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    # ### end Alembic commands ###
