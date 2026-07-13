"""FastAPI Cloud / CLI entrypoint (re-exports the API app)."""

from dss_stock.api.app import app

__all__ = ["app"]
