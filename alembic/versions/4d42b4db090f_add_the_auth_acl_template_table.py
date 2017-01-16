"""add the auth_acl_template table

Revision ID: 4d42b4db090f
Revises: 42abef26feff

"""

# revision identifiers, used by Alembic.
revision = '4d42b4db090f'
down_revision = '42abef26feff'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Column

constraint_name = 'auth_acl_template_template'


def upgrade():
    op.create_table(
        'auth_acl_template',
        Column('id', sa.Integer, primary_key=True),
        Column('template', sa.Text, nullable=False)
    )
    op.create_unique_constraint(constraint_name, 'auth_acl_template', ['template'])
    op.create_table(
        'auth_policy_template',
        Column('policy_uuid', sa.String(38), sa.ForeignKey('auth_policy.uuid', ondelete='CASCADE')),
        Column('template_id', sa.Integer, sa.ForeignKey('auth_acl_template.id', ondelete='CASCADE')),
    )


def downgrade():
    op.drop_table('auth_policy_template')
    op.drop_constraint(constraint_name, 'auth_acl_template')
    op.drop_table('auth_acl_template')
