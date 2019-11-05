"""empty message

Revision ID: 203
Revises:
Create Date: 2019-11-05 17:45:02.915488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '203'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('session', sa.Column('refreshed', sa.DateTime(), nullable=True))
    op.execute("UPDATE session SET refreshed = modified")
    op.add_column("risk", sa.Column("image_data", sa.LargeBinary(), nullable=True))
    op.add_column(
        "risk", sa.Column("image_data_scaled", sa.LargeBinary(), nullable=True)
    )
    op.add_column("risk", sa.Column("image_filename", sa.UnicodeText(), nullable=True))
    op.drop_constraint(u'session_last_publisher_id_fkey', 'session', type_='foreignkey')
    op.drop_constraint(u'session_last_modifier_id_fkey', 'session', type_='foreignkey')
    op.create_foreign_key(None, 'session', 'account', ['last_modifier_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'session', 'account', ['last_publisher_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_index(op.f('ix_tree_has_description'), 'tree', ['has_description'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###