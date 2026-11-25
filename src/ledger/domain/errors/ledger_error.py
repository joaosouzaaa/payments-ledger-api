class LedgerError(Exception):
    """Base class for domain errors. The API layer maps these to HTTP problem responses."""
