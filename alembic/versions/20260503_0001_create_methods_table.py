"""create methods table

Revision ID: 20260503_0001
Revises:
Create Date: 2026-05-03
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260503_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "methods",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("market", sa.String(length=50), nullable=False),
        sa.Column("period", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), server_default="ACTIVE", nullable=False),
        sa.Column("minute_start", sa.Integer(), nullable=False),
        sa.Column("minute_end", sa.Integer(), nullable=False),
        sa.Column("score_filter", sa.String(length=20), nullable=True),
        sa.Column("min_dangerous_attacks", sa.Integer(), nullable=True),
        sa.Column("min_total_shots", sa.Integer(), nullable=True),
        sa.Column("min_shots_on_target", sa.Integer(), nullable=True),
        sa.Column("min_corners", sa.Integer(), nullable=True),
        sa.Column("max_red_cards", sa.Integer(), server_default="0", nullable=False),
        sa.Column("min_odd", sa.Numeric(10, 4), nullable=True),
        sa.Column("max_odd", sa.Numeric(10, 4), nullable=True),
        sa.Column("historical_hit_rate", sa.Numeric(8, 6), nullable=False),
        sa.Column("sample_size", sa.Integer(), nullable=False),
        sa.Column("fair_odd", sa.Numeric(18, 10), nullable=False),
        sa.Column("min_edge", sa.Numeric(10, 4), server_default="0.08", nullable=False),
        sa.Column("stake_units", sa.Numeric(10, 4), server_default="0.5", nullable=False),
        sa.Column("source", sa.String(length=100), server_default="zeus", nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("methods")
