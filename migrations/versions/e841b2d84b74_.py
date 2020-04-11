"""empty message

Revision ID: e841b2d84b74
Revises: 1fb1589943a1
Create Date: 2020-04-10 20:26:41.644802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e841b2d84b74'
down_revision = '1fb1589943a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_username', 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_username', 'users', type_='unique')
    # ### end Alembic commands ###
