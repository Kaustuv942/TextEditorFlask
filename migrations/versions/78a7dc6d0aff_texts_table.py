"""texts table

Revision ID: 78a7dc6d0aff
Revises: 76b003475417
Create Date: 2020-03-25 17:48:25.672132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78a7dc6d0aff'
down_revision = '76b003475417'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('textfile', sa.Column('text', sa.String(length=2500), nullable=True))
    op.drop_column('textfile', 'body')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('textfile', sa.Column('body', sa.VARCHAR(length=2500), nullable=True))
    op.drop_column('textfile', 'text')
    # ### end Alembic commands ###
