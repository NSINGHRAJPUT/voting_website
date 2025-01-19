"""Initial migration with named constraints

Revision ID: 2a3dea8cfb9d
Revises: 
Create Date: 2025-01-14 11:58:39.437225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a3dea8cfb9d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vote', schema=None) as batch_op:
        batch_op.add_column(sa.Column('election_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_election_vote', 'election', ['election_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vote', schema=None) as batch_op:
        batch_op.drop_constraint('fk_election_vote', type_='foreignkey')
        batch_op.drop_column('election_id')

    # ### end Alembic commands ###
