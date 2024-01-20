"""Added tables announcement, comment, category

Revision ID: 55486492a8f4
Revises: 978fb55750b3
Create Date: 2024-01-20 13:56:36.393923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55486492a8f4'
down_revision: Union[str, None] = '978fb55750b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categorys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categorys_id'), 'categorys', ['id'], unique=False)
    op.create_index(op.f('ix_categorys_name'), 'categorys', ['name'], unique=True)
    op.create_table('announcements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categorys.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_announcements_id'), 'announcements', ['id'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_table('categorys_announcements',
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('announcement_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['announcement_id'], ['announcements.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categorys.id'], ),
    sa.PrimaryKeyConstraint('category_id', 'announcement_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('categorys_announcements')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_announcements_id'), table_name='announcements')
    op.drop_table('announcements')
    op.drop_index(op.f('ix_categorys_name'), table_name='categorys')
    op.drop_index(op.f('ix_categorys_id'), table_name='categorys')
    op.drop_table('categorys')
    # ### end Alembic commands ###
