import importlib
import pkgutil

from ledger.db import models
from ledger.db.base import Base


def test_every_model_module_is_exported_from_models_package() -> None:
    """A model not imported in `ledger.db.models.__init__` gets no table in migrations."""
    missing: list[str] = []
    for info in pkgutil.iter_modules(models.__path__):
        module = importlib.import_module(f"{models.__name__}.{info.name}")
        for obj in vars(module).values():
            if (
                isinstance(obj, type)
                and issubclass(obj, Base)
                and obj is not Base
                and obj.__module__ == module.__name__
                and getattr(models, obj.__name__, None) is not obj
            ):
                missing.append(f"{module.__name__}.{obj.__name__}")

    assert not missing, f"Add to ledger/db/models/__init__.py: {missing}"
