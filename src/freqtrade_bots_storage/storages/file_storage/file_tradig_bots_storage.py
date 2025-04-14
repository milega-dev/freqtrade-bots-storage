from typing import Self, Any
import os
import json
from freqtrade_bots_storage.models.bot_state import BotInfo
import uuid_utils
import logging

class FileTradingBotsStorage:
    """
    Storage for trading bots states and configs
    """

    def __init__(self) -> None:
        self.storage_filename: str | None = None

    async def init_storage(self, storage_dir: str) -> Self:
        self.storage_filename = f"{storage_dir}/trading_bots_storage.json"
        logging.info(f"Storage filename: {self.storage_filename}")
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
        if "status" not in bot_config:
            bot_config["status"] = "stopped"

        if "id" not in bot_config:
            bot_id = str(uuid_utils.uuid7())
        else:
            bot_id = bot_config["id"]

        bot_info = BotInfo(
            id=bot_id,
            name=name,
            pair=pair,
            strategy=strategy,
            exchange=exchange,
            status=bot_config["status"],
        )
        config = {
            k: v
            for k, v in bot_config.items()
            if k not in ["id", "name", "pair", "exchange", "strategy", "status"]
        }

        storage_dict = self._get_storage_dict()

        storage_dict["configs"][bot_id] = config
        storage_dict["bots"][bot_id] = bot_info.to_dict()
        storage_dict["states"][bot_id] = {}

        self._save_storage_dict(storage_dict)
        return bot_id


    async def get_bot_full_data_by_id(self, bot_id: str) -> dict[str, Any]:
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
        storage_dict = self._get_storage_dict()
        bots = storage_dict["bots"]
        result = {}

        for bot_id, bot_info in bots.items():
            if (
                (exchanges is None or bot_info["exchange"] in exchanges)
                and (strategies is None or bot_info["strategy"] in strategies)
                and (statuses is None or bot_info["status"] in statuses)
                and (pairs is None or bot_info["pair"] in pairs)
            ):
                result[bot_id] = bot_info

        return result


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
        storage_dict = self._get_storage_dict()
        bots = storage_dict["bots"]
        configs = storage_dict["configs"]
        result = {}

        for bot_id, bot_info in bots.items():
            if (
                (exchanges is None or bot_info["exchange"] in exchanges)
                and (strategies is None or bot_info["strategy"] in strategies)
                and (statuses is None or bot_info["status"] in statuses)
                and (pairs is None or bot_info["pair"] in pairs)
            ):
                result[bot_id] = {**bot_info, **configs[bot_id]}

        return result


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

    async def close(self) -> None: ...
