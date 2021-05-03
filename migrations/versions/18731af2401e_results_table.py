"""results table

Revision ID: 18731af2401e
Revises: 8d34f0f49cb5
Create Date: 2021-05-03 10:39:39.397509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18731af2401e'
down_revision = '8d34f0f49cb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('incorrect', sa.String(length=140), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('results', 'incorrect')
    # ### end Alembic commands ###