import os
from pathlib import Path

from pydantic import BaseModel

from star_rail import constants
from star_rail.utils.functional import color_str, load_json, save_json

__all__ = ["settings", "get_config_status_msg"]

_config_path = Path(constants.CONFIG_PATH, "settings.json")


class Settings(BaseModel):
    FLAG_CHECK_UPDATE: bool = True

    FLAG_GENERATE_XLSX: bool = False

    FLAG_UPATED_COMPLETE: bool = False

    # 旧版本文件名，在更新版本后删除该文件
    OLD_EXE_NAME = ""

    DEFAULT_UID = ""

    class Config:
        extra = "forbid"

    def __setattr__(self, k, v):
        if k not in self.__fields__:
            return
        from star_rail.utils.log import logger

        logger.debug("update config: {} : {} -> {}", k, getattr(self, k), v)
        return super().__setattr__(k, v)

    def __init__(self, **data):
        super().__init__(**data)
        self.load()

    def load(self):
        if not os.path.exists(_config_path):
            return
        local_config = load_json(_config_path)
        self.update(local_config)

    def save(self):
        save_json(_config_path, self.dict())

    def update(self, config_data: dict):
        for k, v in config_data.items():
            setattr(self, k, v)

    def update_and_save(self, config_data: dict):
        self.update(config_data)
        self.save()

    def get(self, key: str):
        return getattr(self, key)

    def set(self, k, v):
        setattr(self, k, v)
        self.save()


settings = Settings()


def get_config_status_msg(key):
    assert hasattr(settings, key)
    return "当前状态: {}".format(
        color_str("打开", "green") if settings.get(key) else color_str("关闭", "red")
    )
