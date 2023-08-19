import os
import sqlite3
import typing

from loguru import logger
from pydantic import BaseModel, Field

from star_rail import constants
from star_rail import exceptions as error
from star_rail.utils import functional

__all__ = [
    "DataBaseModel",
    "DataBaseField",
    "DataBaseClient",
    "model_convert_item",
    "model_convert_list",
]

_default_db_path = os.path.join(constants.DATA_PATH, "star_rail.db")


class DataBaseModel(BaseModel):
    """数据库模型基类
    继承自 pydantic.BaseModel ，只用于 Sqlite ，以成员定义时的类型声明限制数据类型
    """

    __subclass_table__ = []
    """子类注册表"""

    __table_name__ = ""
    """数据库表名"""

    @staticmethod
    def _register(subclass):
        DataBaseModel.__subclass_table__.append(subclass)

    def __init_subclass__(cls):
        cls._register(cls)


def DataBaseField(primary_key=False, **kwargs):
    """数据库模型参数扩展"""
    extra = {"primary_key": primary_key}
    return Field(json_schema_extra=extra, **kwargs)


_T = typing.TypeVar("_T", bound=DataBaseModel)


class ModelAnnotation(BaseModel):
    table_name: str
    column: typing.Set[str] = set()
    primary_key: typing.Set[str] = set()

    @classmethod
    def parse(cls, sub_cls: typing.Type[_T]) -> "ModelAnnotation":
        table_name = getattr(sub_cls, "__table_name__")
        # __table_name__ BaseModel 中存在默认值 ''，使用 not 判断
        if not table_name:
            raise error.DataBaseModelError

        model_anno = ModelAnnotation(table_name=table_name)

        for name, fields in sub_cls.model_fields.items():
            if fields.json_schema_extra and fields.json_schema_extra.get("primary_key", None):
                model_anno.primary_key.add(name)
            model_anno.column.add(name)

        return model_anno


@functional.Singleton()
class DataBaseClient:
    def __init__(self, db_path: str = _default_db_path) -> None:
        self.db_path = db_path
        self.cache: typing.Dict[_T, ModelAnnotation] = dict()

        try:
            self.conn: sqlite3.Connection = sqlite3.connect(self.db_path)
        except sqlite3.Error:
            raise error.DataBaseConnectionError

        self.conn.row_factory = sqlite3.Row

        if db_path == ":memory:":
            pass
        elif not os.path.exists(self.db_path):
            os.makedirs(os.path.split(self.db_path)[0], exist_ok=True)

        logger.debug("database file path : {}", self.db_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.commit()

        if exc_type:
            self.conn.rollback()
            raise error.DataBaseExecuteError

    def commit(self):
        self.conn.commit()

    def close_all(self):
        self.conn.commit()
        self.conn.close()

    def select(self, sql_script, *args):
        """通过命名占位符查询"""
        logger.debug("[SQL] [SELECT] : {}, [param]: {}", sql_script, args)
        return self.conn.cursor().execute(sql_script, args)

    def insert(self, item: _T, mode: typing.Literal["ignore", "update", "none"] = "none"):
        cls_anno = self.parse_model(type(item))

        if mode == "none":
            mode = ""
        elif mode == "ignore":
            mode = " or ignore "
        elif mode == "update":
            mode = " or replace "

        columns = ",".join(cls_anno.column)
        placeholders = ",".join(["?" for _ in cls_anno.column])
        values = [getattr(item, k) for k in cls_anno.column]

        sql = """insert {} into {} ({}) values ({}) ;""".format(
            mode, cls_anno.table_name, columns, placeholders
        )
        logger.debug("[SQL] [INSERT] : {}", sql)
        cur = self.conn.cursor().execute(sql, values)
        self.commit()
        return cur

    def insert_batch(
        self, items: typing.List[_T], mode: typing.Literal["ignore", "update", "none"] = "none"
    ):
        if len(items) == 0:
            return

        cls_anno = self.parse_model(type(items[0]))

        if mode == "none":
            mode = ""
        elif mode == "ignore":
            mode = " or ignore "
        elif mode == "update":
            mode = " or replace "

        columns = ",".join(cls_anno.column)
        placeholders = ",".join(["?" for _ in cls_anno.column])
        values = []
        for item in items:
            item_values = [getattr(item, k) for k in cls_anno.column]
            values.append(item_values)

        sql_temp = """ insert {} into {} ({}) values ({}) ;""".format(
            mode, cls_anno.table_name, columns, placeholders
        )
        logger.debug("[SQL] [INSERT] : {}", sql_temp)
        cur = self.conn.cursor().executemany(sql_temp, values)
        self.commit()
        return cur

    def parse_model(self, item_type: typing.Type[_T]) -> ModelAnnotation:
        if item_type in self.cache:
            return self.cache[item_type]
        cls_anno = ModelAnnotation.parse(item_type)
        if item_type not in self.cache:
            self.cache[item_type] = cls_anno
        return cls_anno

    def create_all(self):
        """创建已注册的所有表"""
        for sub_cls in DataBaseModel.__subclass_table__:
            model_anno = self.parse_model(sub_cls)

            if model_anno is None:
                continue
            sql = """create table if not exists {} ({}, primary key ({}) );""".format(
                model_anno.table_name, ",".join(model_anno.column), ",".join(model_anno.primary_key)
            )
            logger.debug("[SQL] [CREATE] : {}", sql)
            self.cache[sub_cls] = model_anno
            self.conn.cursor().execute(sql)
            self.commit()


def model_convert_item(
    row: typing.Optional[sqlite3.Row], sub_cls: typing.Type[_T]
) -> typing.Optional[_T]:
    if row is None:
        return None
    data = {k: row[k] for k in row.keys()}
    return sub_cls(**data)


def model_convert_list(
    row: typing.Optional[typing.List[sqlite3.Row]], sub_cls: typing.Type[_T]
) -> typing.Optional[typing.List[_T]]:
    if row is None:
        return None

    data = []

    for item in row:
        t = sub_cls(**{k: item[k] for k in item.keys()})
        data.append(t)
    return data
