"""freqtrade-bots-storage package."""

# Import the FileTradingBotsStorage class to expose it at the package root level
from .storages.file_storage.file_tradig_bots_storage import FileTradingBotsStorage

__all__ = ["FileTradingBotsStorage"]
