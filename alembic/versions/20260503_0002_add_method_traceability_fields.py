"""add method traceability fields

Revision ID: 20260503_0002
Revises: 20260503_0001
Create Date: 2026-05-03
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260503_0002"
down_revision: str | None = "20260503_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("methods", sa.Column("zeus_query", sa.Text(), nullable=True))
    op.add_column("methods", sa.Column("scanner_condition", sa.Text(), nullable=True))
    op.add_column("methods", sa.Column("entry_rule", sa.Text(), nullable=True))
    op.add_column("methods", sa.Column("validation_notes", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("methods", "validation_notes")
    op.drop_column("methods", "entry_rule")
    op.drop_column("methods", "scanner_condition")
    op.drop_column("methods", "zeus_query")
