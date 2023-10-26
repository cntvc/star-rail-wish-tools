import enum
import glob
import os
import re
from pathlib import Path

from star_rail import exceptions as error
from star_rail.module import Account
from star_rail.utils.log import logger

from .types import GameBiz

MHY_LOG_ROOT_PATH = os.path.join(os.getenv("USERPROFILE"), "AppData", "LocalLow")


class GameLogPath(str, enum.Enum):
    CN = "miHoYo/崩坏：星穹铁道/"
    GLOBAL = "Cognosphere/Star Rail/"

    @staticmethod
    def get_by_user(user: Account):
        if user.game_biz == GameBiz.CN.value:
            return Path(MHY_LOG_ROOT_PATH, GameLogPath.CN.value, "Player.log")
        elif user.game_biz == GameBiz.GLOBAL.value:
            return Path(MHY_LOG_ROOT_PATH, GameLogPath.GLOBAL.value, "Player.log")


class GameClient:
    def __init__(self, user: Account) -> None:
        self.user = user

    def get_game_path(self):
        """解析日志文件获取游戏路径"""
        log_path = GameLogPath.get_by_user(self.user)
        if not log_path.exists():
            raise error.HsrException("Game log file not found")

        try:
            log_text = log_path.read_text(encoding="utf8")
        except UnicodeDecodeError as err:
            logger.debug(f"file encoding format is not utf8, try to use default encoding \n {err}")
            log_text = log_path.read_text(encoding=None)

        res = re.search("([A-Z]:/.+StarRail_Data)", log_text)
        game_path = res.group() if res else None
        return game_path

    def get_webcache_path(self):
        """在游戏文件夹中查找 Web 缓存文件"""
        game_path = self.get_game_path()
        if not game_path:
            raise error.HsrException("Game path not found")
        cache_root_path = os.path.join(game_path, "webCaches")
        data_2_files = glob.glob(os.path.join(cache_root_path, "*", "Cache/Cache_Data/data_2"))
        if not data_2_files:
            raise error.HsrException("Game web cache file not found")
        data_2_files = sorted(data_2_files, key=lambda file: os.path.getmtime(file), reverse=True)

        return data_2_files[0]
