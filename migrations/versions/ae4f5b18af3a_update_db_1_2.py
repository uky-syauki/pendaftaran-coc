"""update db 1.2

Revision ID: ae4f5b18af3a
Revises: 
Create Date: 2024-01-05 22:43:49.236241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae4f5b18af3a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_admin_username'), ['username'], unique=False)

    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nama_lengkap', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('nomor_wa', sa.String(length=20), nullable=True),
    sa.Column('asal_kampus', sa.String(length=64), nullable=True),
    sa.Column('bukti_tf', sa.String(length=64), nullable=True),
    sa.Column('bukti_follow', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('email', name='unique_email'),
    sa.UniqueConstraint('nomor_wa'),
    sa.UniqueConstraint('nomor_wa', name='unique_nomor_wa')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_admin_username'))

    op.drop_table('admin')
    # ### end Alembic commands ###