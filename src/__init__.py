from importlib.metadata import metadata
from .manager import HistoricalDataManager

meta = metadata("fyers-history")

__all__ = ["HistoricalDataManager"]

__license__ = meta.get("License", "MIT")

__version__ = "0.1.0"