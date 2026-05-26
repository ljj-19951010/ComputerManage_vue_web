"""baseline

Revision ID: 989a67ada6d6
Revises: acbf5d1037fe
Create Date: 2026-05-26 10:39:46.769302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '989a67ada6d6'
down_revision: Union[str, Sequence[str], None] = 'acbf5d1037fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
