"""init

Revision ID: f7d9f3e6ac1a
Revises:
Create Date: 2025-05-27 16:44:14.958849+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.alembic.migrations.utils import get_existing_tables
from sqlalchemy_fields.types import UUIDType, URLType
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.backend.leaderboard import entities as leaderbard_entities

# revision identifiers, used by Alembic.
revision: str = "f7d9f3e6ac1a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    existing_tables = set(get_existing_tables())  # noqa: F841

    if leaderbard_entities.LeaderBoardLog.__tablename__ not in existing_tables:
        pass



def downgrade() -> None:
    existing_tables = set(get_existing_tables())  # noqa: F841

    if leaderbard_entities.LeaderBoardLog.__tablename__ in existing_tables:
        pass
