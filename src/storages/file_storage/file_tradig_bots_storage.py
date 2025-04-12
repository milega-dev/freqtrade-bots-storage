from typing import Self, Any
import os
import json
from src.models.bot_state import BotState


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
            with open(self.storage_filename, "w") as f:
                json.dump({
                    "states": {},
                    "configs": {},
                    "detailed_states": {},
                }, f)
        return self

    
    def _get_storage_dict(self) -> dict[str, Any]:
        with open(self.storage_filename, "r") as f:
            return json.load(f)

    
    def _save_storage_dict(self, storage_dict: dict[str, Any]) -> None:
        with open(self.storage_filename, "w") as f:
            json.dump(storage_dict, f)


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

        bot_state = BotState(
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
        storage_dict["states"][bot_id] = bot_state.to_dict()
        storage_dict["detailed_states"][bot_id] = {}
        
        self._save_storage_dict(storage_dict)
        return bot_config["id"]


    async def get_bot_by_id(self, bot_id: str) -> dict[str, Any]:
        ...
        
    async def get_bot_by_exchange_and_pair(self, exchange: str, pair: str) -> dict[str, Any]:
        ...
        
    async def get_bots_list(self) -> list[dict[str, Any]]:
        ...
    
    async def delete_bot(self, bot_id: str) -> None:
        ...
    
    async def update_bot(self, bot_id: str, config: dict[str, Any]) -> None:
        ...
    
    async def close(self) -> None:
        ...
    

