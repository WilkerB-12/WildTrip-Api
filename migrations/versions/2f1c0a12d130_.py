"""empty message

Revision ID: 2f1c0a12d130
Revises: 9206b1fc2f6d
Create Date: 2022-03-31 18:33:57.830584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f1c0a12d130'
down_revision = '9206b1fc2f6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company_user', sa.Column('address', sa.String(length=80), nullable=True))
    op.add_column('company_user', sa.Column('instagram_url', sa.String(length=80), nullable=False))
    op.drop_constraint('company_user_Instagram_url_key', 'company_user', type_='unique')
    op.create_unique_constraint(None, 'company_user', ['instagram_url'])
    op.create_unique_constraint(None, 'company_user', ['company_name'])
    op.drop_column('company_user', 'adress')
    op.drop_column('company_user', 'Instagram_url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company_user', sa.Column('Instagram_url', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
    op.add_column('company_user', sa.Column('adress', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'company_user', type_='unique')
    op.drop_constraint(None, 'company_user', type_='unique')
    op.create_unique_constraint('company_user_Instagram_url_key', 'company_user', ['Instagram_url'])
    op.drop_column('company_user', 'instagram_url')
    op.drop_column('company_user', 'address')
    # ### end Alembic commands ###
