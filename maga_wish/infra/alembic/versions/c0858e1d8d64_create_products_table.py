"""create products table

Revision ID: c0858e1d8d64
Revises: d2ce70739f1e
Create Date: 2025-03-10 18:56:52.536899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0858e1d8d64'
down_revision: Union[str, None] = 'd2ce70739f1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'products',
        sa.Column('id', sa.UUID(), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('image', sa.String(500), nullable=True),
        sa.Column('brand', sa.String(255), nullable=True),
        sa.Column('reviewScore', sa.Float(), nullable=True),
        sa.Column('description', sa.String(500), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('products')
