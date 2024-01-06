"""s 1.4

Revision ID: eb2cedb259e3
Revises: ae4f5b18af3a
Create Date: 2024-01-06 11:20:39.327020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb2cedb259e3'
down_revision = 'ae4f5b18af3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_email', ['email'])
        batch_op.create_unique_constraint('unique_nomor_wa', ['nomor_wa'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('unique_nomor_wa', type_='unique')
        batch_op.drop_constraint('unique_email', type_='unique')

    # ### end Alembic commands ###