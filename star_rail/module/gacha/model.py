import enum
import time

from pydantic import BaseModel

from star_rail import __version__ as version
from star_rail import constants
from star_rail.i18n import i18n
from star_rail.utils import functional


class GachaType(str, enum.Enum):
    REGULAR_WARP = "1"
    STARTER_WARP = "2"
    CHARACTER_EVENT_WARP = "11"
    LIGHT_CONE_EVENT_WARP = "12"

    @staticmethod
    def dict():
        return {
            GachaType.REGULAR_WARP.value: i18n.regular_warp,
            GachaType.STARTER_WARP.value: i18n.starter_warp,
            GachaType.CHARACTER_EVENT_WARP.value: i18n.character_event_warp,
            GachaType.LIGHT_CONE_EVENT_WARP.value: i18n.light_cone_event_warp,
        }

    @staticmethod
    def list():
        return [member.value for member in GachaType]


SRGF_VERSION = "1.0.0"


class GachaInfo(BaseModel):
    uid: str
    lang: str
    export_timestamp: int
    export_time: str
    export_app: str
    export_app_version: str

    @staticmethod
    def gen(uid: str, lang: str):
        std_time = time.time()
        format_time = functional.get_format_time(std_time)
        return GachaInfo(
            uid=uid,
            lang=lang,
            export_timestamp=int(std_time),
            export_time=format_time,
            export_app=constants.APP_NAME,
            export_app_version=version,
        )

    @staticmethod
    def gen_to_srgf(uid: str, lang: str):
        info = GachaInfo.gen(uid, lang)
        info["srgf_version"] = SRGF_VERSION
        return info
