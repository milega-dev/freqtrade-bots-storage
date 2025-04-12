from typing import Any, Protocol


class TradingBotsStorageProtocol(Protocol):
    async def put_bot(self, bot_id: str, config: dict[str, Any]) -> str:
        """
        Add new bot to storage
        Returns bot_id
        """
        ...

    async def get_bot_full_data_by_id(self, bot_id: str) -> dict[str, Any]: ...


    async def get_bots(
        self,
        exchanges: list[str] | None = None,
        strategies: list[str] | None = None,
        statuses: list[str] | None = None,
        pairs: list[str] | None = None,
    ) -> dict[str, dict[str, Any]]:
        """
        Returns dict of bots - key is bot_id, value is bot_info
        """
        ...

    async def get_bots_with_configs(
        self,
        exchanges: list[str] | None = None,
        strategies: list[str] | None = None,
        statuses: list[str] | None = None,
        pairs: list[str] | None = None,
    ) -> dict[str, dict[str, Any]]:
        """
        Returns dict of bots - key is bot_id, value is dict with bot_info and config
        """
        ...

    async def delete_bot(self, bot_id: str) -> None: ...

    async def update_bot_state(self, bot_id: str, update: dict[str, Any]) -> None: ...

    async def update_bot_config(self, bot_id: str, update: dict[str, Any]) -> None: ...

    async def update_bot_status(self, bot_id: str, status: str) -> None: ...

    async def close(self) -> None: ...
