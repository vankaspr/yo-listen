"""Create CommentLike table and update User ando Comment

Revision ID: 6522a86630e9
Revises: bc9ff92ba19c
Create Date: 2025-11-06 15:26:24.904296

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6522a86630e9"
down_revision: Union[str, Sequence[str], None] = "bc9ff92ba19c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.create_table(
        "comment_likes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("comment_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["comment_id"],
            ["comments.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id", "comment_id", name="unique_user_comment_like"
        ),
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_table("comment_likes")
    
