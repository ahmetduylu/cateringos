"""Initial schema: users, leads, lead_logs

Revision ID: 001
Revises:
Create Date: 2026-02-25
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- users tablosu ---
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ad", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("rol", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    # --- leads tablosu ---
    op.create_table(
        "leads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("isletme_adi", sa.String(length=255), nullable=False),
        sa.Column("telefon", sa.String(length=50), nullable=True),
        sa.Column("adres", sa.Text(), nullable=True),
        sa.Column("harita_linki", sa.Text(), nullable=True),
        sa.Column(
            "eklenme_tarihi",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("assigned_user_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="havuzda"),
        sa.ForeignKeyConstraint(["assigned_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_leads_id"), "leads", ["id"], unique=False)
    op.create_index(op.f("ix_leads_telefon"), "leads", ["telefon"], unique=False)
    op.create_index(op.f("ix_leads_assigned_user_id"), "leads", ["assigned_user_id"], unique=False)

    # --- lead_logs tablosu ---
    op.create_table(
        "lead_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("lead_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("islem_turu", sa.String(length=50), nullable=False),
        sa.Column("aciklama", sa.Text(), nullable=True),
        sa.Column(
            "tarih",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_lead_logs_id"), "lead_logs", ["id"], unique=False)
    op.create_index(op.f("ix_lead_logs_lead_id"), "lead_logs", ["lead_id"], unique=False)


def downgrade() -> None:
    op.drop_table("lead_logs")
    op.drop_table("leads")
    op.drop_table("users")
