from typing import Any, Protocol


class TradingBotsStorageProtocol(Protocol):
    async def put_bot(self, bot_id: str, config: dict[str, Any]) -> str:
        """
        Add new bot to storage
        Returns bot_id
        """
        ...
    
    async def get_bot_by_id(self, bot_id: str) -> dict[str, Any]:
        ...

    async def get_active_bot_by_exchange_and_pair(self, exchange: str, pair: str) -> dict[str, Any] | None:
        ...

    async def get_all_bots(self) -> dict[str, dict[str, Any]]:
        """
        Returns dict of bots - key is bot_id, value is bot_info
        """
        ...
        
    async def delete_bot(self, bot_id: str) -> None:
        ...
    
    async def update_bot(self, bot_id: str, config: dict[str, Any]) -> None:
        ...

    async def close(self) -> None:
        ...