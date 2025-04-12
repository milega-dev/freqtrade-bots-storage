from typing import Self, Any
import os
import json
from freqtrade_bots_storage.models.bot_state import BotInfo


class FileTradingBotsStorage():
    """
    Storage for trading bots states and configs
    """
    def __init__(self) -> None:
        ...

    async def create_storage(self, storage_dir: str) -> Self:
        self.storage_filename = f"{storage_dir}/trading_bots_storage.json"
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        if not os.path.exists(self.storage_filename):
            storage_dict = {
                "bots": {},
                "configs": {},
                "states": {},
            }
            self._save_storage_dict(storage_dict)
        return self

    
    def _get_storage_dict(self) -> dict[str, Any]:
        with open(self.storage_filename, "r") as f:
            return json.load(f)

    
    def _save_storage_dict(self, storage_dict: dict[str, Any]) -> None:
        with open(self.storage_filename, "w") as f:
            json.dump(storage_dict, f, indent=2)


    async def put_bot(self, bot_config: dict[str, Any]) -> str:
        """
        Add new bot to storage
        Returns bot_id
        """
        name = bot_config["name"]
        pair = bot_config["pair"]
        exchange = bot_config["exchange"]
        strategy = bot_config["strategy"]
        status = "stopped"
        bot_id = bot_config["id"]

        bot_info = BotInfo(
            id=bot_id,
            name=name,
            pair=pair,
            strategy=strategy,
            exchange=exchange,
            status=status,
        )
        config = { k: v for k, v in bot_config.items() if k not in ["id", "name", "pair", "exchange", "strategy", "status"]}
        
        storage_dict = self._get_storage_dict()

        storage_dict["configs"][bot_id] = config
        storage_dict["bots"][bot_id] = bot_info.to_dict()
        storage_dict["states"][bot_id] = {}
        
        self._save_storage_dict(storage_dict)
        return bot_config["id"]


    async def get_bot_by_id(self, bot_id: str) -> dict[str, Any]:
        """
        Get bot by id
        Returns bot_info, config, state
        """
        storage_dict = self._get_storage_dict()
        bot_info = storage_dict["bots"].get(bot_id)
        if bot_info is None:
            raise ValueError(f"Bot with id {bot_id} not found")

        config = storage_dict["configs"].get(bot_id)
        state = storage_dict["states"].get(bot_id)
        return {"bot": bot_info, "config": config, "state": state}
        
    async def get_active_bot_by_exchange_and_pair(self, exchange: str, pair: str) -> dict[str, Any] | None:
        storage_dict = self._get_storage_dict()
        for bot_id, bot_info in storage_dict["bots"].items():
            if bot_info["exchange"] == exchange and bot_info["pair"] == pair and bot_info["status"] == "running":
                return self.get_bot_by_id(bot_id)
        return None
        
    async def get_bots_list(self) -> list[dict[str, Any]]:
        """
        Returns list of bots
        """
        storage_dict = self._get_storage_dict()
        return list(storage_dict["bots"].values())
    

    async def delete_bot(self, bot_id: str) -> None:
        storage_dict = self._get_storage_dict()
        del storage_dict["bots"][bot_id]
        del storage_dict["configs"][bot_id]
        del storage_dict["states"][bot_id]
        self._save_storage_dict(storage_dict)
    

    async def update_bot_state(self, bot_id: str, update: dict[str, Any]) -> None:
        storage_dict = self._get_storage_dict()
        bot_info = storage_dict["bots"].get(bot_id)
        if bot_info is None:
            raise ValueError(f"Bot with id {bot_id} not found")

        state = storage_dict["states"].get(bot_id)
        if state is None:
            state = {}
        
        storage_dict["states"][bot_id] = {**state, **update}
        self._save_storage_dict(storage_dict)


    async def update_bot_config(self, bot_id: str, update: dict[str, Any]) -> None:
        storage_dict = self._get_storage_dict()
        config = storage_dict["configs"].get(bot_id)
        if config is None:
            raise ValueError(f"Config for bot with id {bot_id} not found")
        
        storage_dict["configs"][bot_id] = {**config, **update}
        self._save_storage_dict(storage_dict)


    async def update_bot_status(self, bot_id: str, status: str) -> None:
        storage_dict = self._get_storage_dict()
        bot_info = storage_dict["bots"].get(bot_id)
        if bot_info is None:
            raise ValueError(f"Bot with id {bot_id} not found")
        
        storage_dict["bots"][bot_id] = {**bot_info, "status": status}
        self._save_storage_dict(storage_dict)

    
    async def close(self) -> None:
        ...
    

