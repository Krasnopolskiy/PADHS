"""Add contract table

Revision ID: 4c124e3db2f4
Revises: 
Create Date: 2024-03-26 18:30:51.054020

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from database.entity.contract import AddressEncoder

# revision identifiers, used by Alembic.
revision: str = "4c124e3db2f4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "contract",
        sa.Column("address", AddressEncoder(length=20), nullable=False),
        sa.Column("status", sa.Enum("CREATED", "PROCESS", "SUCCESS", "ERROR", name="status"), nullable=False),
        sa.Column("source", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("address"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("contract")
    # ### end Alembic commands ###
