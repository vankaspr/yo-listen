"""Update relathionship

Revision ID: 3a86cfe4dcab
Revises: 6522a86630e9
Create Date: 2025-11-06 16:26:43.417144

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3a86cfe4dcab"
down_revision: Union[str, Sequence[str], None] = "6522a86630e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        op.f("comment_likes_comment_id_fkey"),
        "comment_likes",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None,
        "comment_likes",
        "comments",
        ["comment_id"],
        ["id"],
        ondelete="CASCADE",
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "comment_likes", type_="foreignkey")
    op.create_foreign_key(
        op.f("comment_likes_comment_id_fkey"),
        "comment_likes",
        "comments",
        ["comment_id"],
        ["id"],
    )
