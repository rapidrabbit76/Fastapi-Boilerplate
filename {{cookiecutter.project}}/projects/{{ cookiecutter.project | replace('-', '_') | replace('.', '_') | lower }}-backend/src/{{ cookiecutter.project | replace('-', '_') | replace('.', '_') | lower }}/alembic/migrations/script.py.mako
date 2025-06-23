"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.alembic.migrations.utils import get_existing_tables
from sqlalchemy_fields.types import UUIDType,URLType
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    existing_tables = set(get_existing_tables())  # noqa: F841
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    existing_tables = set(get_existing_tables())  # noqa: F841
    ${downgrades if downgrades else "pass"}