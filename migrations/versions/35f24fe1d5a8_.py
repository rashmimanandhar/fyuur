"""empty message

Revision ID: 35f24fe1d5a8
Revises: 49da96fc1110
Create Date: 2021-03-13 15:51:14.123264

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '35f24fe1d5a8'
down_revision = '49da96fc1110'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=True)
    op.alter_column('Artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###
