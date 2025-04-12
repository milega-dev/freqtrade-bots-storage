"""freqtrade-bots-storage package."""

# Import the FileTradingBotsStorage class to expose it at the package root level
from .storages.file_storage.file_tradig_bots_storage import FileTradingBotsStorage
from .protocol.protocol import TradingBotsStorageProtocol
from .models.bot_state import BotInfo

__all__ = ["FileTradingBotsStorage", "TradingBotsStorageProtocol", "BotInfo"]
