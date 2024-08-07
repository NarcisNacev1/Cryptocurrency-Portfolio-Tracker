"""Initial migration

Revision ID: f2994954a0f7
Revises: 4d7b97308c95
Create Date: 2024-08-07 15:42:51.794256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2994954a0f7'
down_revision = '4d7b97308c95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('portfolio_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('value', sa.Numeric(precision=20, scale=8), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('cryptocurrency', sa.String(length=50), nullable=False),
    sa.Column('amount', sa.Numeric(precision=20, scale=8), nullable=False),
    sa.Column('transaction_type', sa.String(length=4), nullable=False),
    sa.Column('transaction_price', sa.Numeric(precision=20, scale=8), nullable=False),
    sa.Column('transaction_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('transaction')
    op.drop_table('portfolio_history')
    # ### end Alembic commands ###
