import os
from alembic import op
from sqlalchemy import Inspector
import uuid


def get_existing_tables() -> list[str]:
    con = op.get_bind()
    inspector = Inspector.from_engine(con)
    response = []
    response.extend(inspector.get_table_names())
    response.extend(get_existing_mv())
    return response


def get_existing_mv() -> list[str]:
    con = op.get_bind()
    inspector = Inspector.from_engine(con)
    response = []
    # response.extend(inspector.get_materialized_view_names())
    response.extend(inspector.get_view_names())
    return response


def get_revision_id():
    return str(uuid.uuid4()).replace("-", "")[:12]


def run():
    print("********** Running migrations... **********")
    try:
        from alembic import command
        from alembic.config import Config

        print(os.getcwd())
        alembic_cfg = Config("alembic.ini")

        # Set the script location dynamically
        # migrations_path = "src/migration"
        # alembic_cfg.set_main_option("script_location", str(migrations_path))
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("********** migrations complete **********")
