"""Added unique_link column

Revision ID: 26253dc72ac5
Revises: 
Create Date: 2024-04-22 10:58:20.181409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26253dc72ac5'
down_revision = None
branch_labels = None
depends_on = None


# def upgrade():
#     with op.batch_alter_table('admin', schema=None) as batch_op:
#         batch_op.add_column(sa.Column('unique_link', sa.String(length=100), nullable=True))
#         batch_op.create_unique_constraint(None, ['unique_link'])



# def downgrade():
#     with op.batch_alter_table('admin', schema=None) as batch_op:
#         batch_op.drop_constraint(None, type_='unique')
#         batch_op.drop_column('unique_link')

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unique_link', sa.String(length=100), nullable=True))
        batch_op.create_unique_constraint('uq_admin_unique_link', ['unique_link'])
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_constraint('uq_admin_unique_link', type_='unique')
        batch_op.drop_column('unique_link')
    # ### end Alembic commands ###
