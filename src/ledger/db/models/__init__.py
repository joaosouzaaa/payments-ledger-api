"""Importing this package registers every model on `Base.metadata`.

Add each new model here: Alembic autogenerate and the test schema only see imported models.
"""

from ledger.db.models.account import Account

__all__ = ["Account"]
