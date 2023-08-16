import os
import sqlite3
import typing

from pydantic import BaseModel

from star_rail.constants import DATA_PATH
from star_rail.exceptions import DBConnectionError, ParamTypeError
from star_rail.i18n import i18n
from star_rail.utils.functional import Singleton
from star_rail.utils.log import logger

from .base_model import DBModel

__all__ = ["init_all_table", "convert", "DBClient"]


class SqlFields(BaseModel):
    """创建数据库模型的数据"""

    table_name: str
    cloumn: typing.Set[str] = set()
    primary_key: typing.Set[str] = set()


def _parse_sql_fields(cls: DBModel) -> SqlFields:
    table_name = getattr(cls, "__table_name__", None)
    if table_name:
        sql_fields = SqlFields(table_name=table_name)
    else:
        return None
    for name, fields in cls.model_fields.items():
        if fields.json_schema_extra and fields.json_schema_extra.get("primary_key", None):
            sql_fields.primary_key.add(name)
        sql_fields.cloumn.add(name)

    if not sql_fields.primary_key:
        # 因为从数据库映射到 pydantic.BaseModel ，在插入数据无法处理主键值
        # 这里为每个模型自动添加一个字段为 id 作为主键
        # 如果没设置主键，添加一个自增主键
        id = "id"
        sql_fields.cloumn.add(id)
        sql_fields.primary_key.add(id)

    return sql_fields


_default_db_path = os.path.join(DATA_PATH, "star_rail.db")


@Singleton()
class DBClient:
    def __init__(self, db_path: str = _default_db_path) -> None:
        self._db_path = db_path
        os.makedirs(os.path.split(db_path)[0], exist_ok=True)
        logger.debug("database file path : {}", self._db_path)
        self._cache: typing.Dict[object, SqlFields] = dict()
        try:
            self._conn = sqlite3.connect(self._db_path)
        except sqlite3.Error:
            raise DBConnectionError
        self._conn.row_factory = sqlite3.Row

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.commit()

    @property
    def conn(self):
        return self._conn

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.commit()
        self._conn.close()

    def execute_sql(self, sql_script):
        """一次执行多个 sql 语句，以 `;` 分隔"""
        return self.conn.executescript(sql_script)

    def select(self, sql_script):
        return self._conn.cursor().execute(sql_script)

    def insert(self, item: DBModel, mode: typing.Literal["ignore", "update", "none"] = "none"):
        """插入一个 DBModel 对象"""
        item_type = type(item)
        self._update_cache(item_type)
        sql_field = self._cache[item_type]

        if mode == "none":
            mode = ""
        elif mode == "ignore":
            mode = " or ignore "
        elif mode == "update":
            mode = " or replace "

        colunms = ",".join(sql_field.cloumn)
        placeholders = ",".join(["?" for _ in sql_field.cloumn])
        values = [getattr(item, k) for k in sql_field.cloumn]

        sql = """insert {} into {} ({}) values ({})
        """.format(
            mode, sql_field.table_name, colunms, placeholders
        )
        logger.debug("[SQL] [insert] : {}", sql)
        cur = self._conn.cursor().execute(sql, values)
        self.commit()
        return cur

    def insert_batch(
        self, items: typing.List[DBModel], mode: typing.Literal["ignore", "update", "none"] = "none"
    ):
        if len(items) == 0:
            return True

        item_type = type(items[0])
        self._update_cache(item_type)
        sql_field = self._cache[item_type]

        if mode == "none":
            mode = ""
        elif mode == "ignore":
            mode = " or ignore "
        elif mode == "update":
            mode = " or replace "

        colunms = ",".join(sql_field.cloumn)
        placeholders = ",".join(["?" for _ in sql_field.cloumn])
        values = []
        for item in items:
            item_values = [getattr(item, k) for k in sql_field.cloumn]
            values.append(item_values)

        sql_temp = """
        insert {} into {} ({}) values ({})
        """.format(
            mode, sql_field.table_name, colunms, placeholders
        )
        logger.debug("[SQL] [insert] : {}", sql_temp)
        self.conn.cursor().executemany(sql_temp, values)
        self.commit()

    def _update_cache(self, item_type: typing.Type[DBModel]):
        if item_type in self._cache:
            return
        sql_field = _parse_sql_fields(item_type)
        if sql_field is None:
            return
        if item_type not in self._cache:
            self._cache[item_type] = sql_field


def init_all_table(db: DBClient):
    """根据注册的模型创建数据库"""
    for cls in DBModel.__sql_table__:
        sql_field = _parse_sql_fields(cls)
        if sql_field is None:
            continue
        sql = """create table if not exists {} ({}, primary key ({}))""".format(
            sql_field.table_name, ",".join(sql_field.cloumn), ",".join(sql_field.primary_key)
        )
        db._cache[cls] = sql_field
        db.execute_sql(sql)
    db.commit()


def convert(query_res: typing.Union[typing.List, sqlite3.Row], item_type: typing.Type[DBModel]):
    """查询结果转换"""
    if not query_res:
        return None
    if isinstance(query_res, typing.List):
        return _convert_list(query_res, item_type)
    elif isinstance(query_res, sqlite3.Row):
        return _convert_item(query_res, item_type)
    else:
        raise ParamTypeError(i18n.error.param_type_error, type(query_res))


def _convert_list(query_res: typing.List, item_type: typing.Type[DBModel]):
    return [_convert_item(item, item_type) for item in query_res]


def _convert_item(query_res: sqlite3.Row, item_type: typing.Type[DBModel]):
    d = {}
    for k in query_res.keys():
        d[k] = query_res[k]
    return item_type(**d)
