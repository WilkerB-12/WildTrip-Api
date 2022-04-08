"""empty message

Revision ID: d9eeef254c14
Revises: 1120974f5175
Create Date: 2022-04-07 21:13:18.891512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9eeef254c14'
down_revision = '1120974f5175'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company_post', sa.Column('phone_number', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'company_post', ['phone_number'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'company_post', type_='unique')
    op.drop_column('company_post', 'phone_number')
    # ### end Alembic commands ###
