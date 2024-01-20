from rich.columns import Columns
from rich.console import RenderableType
from rich.markdown import Markdown
from rich.panel import Panel
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Static, TabbedContent, TabPane

from star_rail.config import settings
from star_rail.module import HSRClient
from star_rail.module.record.model import AnalyzeResult
from star_rail.module.record.types import GACHA_TYPE_DICT, GachaRecordType
from star_rail.tui.handler import error_handler, required_account
from star_rail.tui.widgets import SimpleButton, apply_text_color

RECORD_TMP = """# 抽卡总数: {}\t\t 5星总数: {}\t\t 保底计数: {}"""
EMPTY_DATA = [
    r"[O]     \,`/ /      [/O]",
    r"[O]    _)..  `_     [/O]",
    r"[O]   ( __  -\      [/O]",
    r"[O]       '`.       [/O]",
    r"[O]      ( \>_-_,   [/O]",
    r"[O]      _||_ ~-/   [G]No data at the moment![/G][/O]",
]


class GachaContent(Horizontal):
    def __init__(self, desc: str, val, **kwargs):
        super().__init__(**kwargs)
        self.desc = desc
        self.val = val

    def compose(self) -> ComposeResult:
        yield Static(self.desc, id="desc")
        yield Static(self.val, id="value")


class EmptyData(Container):
    def compose(self) -> ComposeResult:
        with Center():
            yield Static(apply_text_color(EMPTY_DATA))


class RecordDetail(Container):
    def __init__(self, analyze_result: AnalyzeResult, **kwargs):
        super().__init__(**kwargs)
        self.analyze_result = analyze_result

    def compose(self) -> RenderableType:
        with TabbedContent():
            for result in self.analyze_result.data:
                if (
                    not settings.DISPLAY_STARTER_WARP
                    and result.gacha_type == GachaRecordType.STARTER_WARP.value
                ):
                    continue
                name = GACHA_TYPE_DICT[result.gacha_type]
                with TabPane(name):
                    yield Static(
                        Markdown(
                            RECORD_TMP.format(
                                result.total_count, len(result.rank_5), result.pity_count
                            )
                        )
                    )
                    with VerticalScroll():
                        rank_5_list = [
                            Panel(f"{i}. " + item.name + " : " + item.index + "抽", expand=True)
                            for i, item in enumerate(result.rank_5, start=1)
                        ]
                        yield Static(Columns(rank_5_list))


class GachaRecordDialog(Container):
    analyze_result: reactive[AnalyzeResult] = reactive(None, layout=True)

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield SimpleButton("刷新记录", id="refresh_with_cache")
            # yield Button("读取链接", id="refresh_with_url")
            yield SimpleButton("导入数据", id="import")
            yield SimpleButton("生成Execl", id="export_execl")
            yield SimpleButton("生成SRGF", id="export_srgf")

    def watch_analyze_result(self, new):
        def remove_widgets():
            empty_data = self.query(EmptyData)
            if empty_data:
                empty_data.remove()
            details = self.query(RecordDetail)
            if details:
                details.remove()

        remove_widgets()

        if not new:
            self.mount(EmptyData(id="empty_record"))
            return

        self.mount(RecordDetail(new))

    @work(exclusive=True)
    @on(SimpleButton.Pressed, "#refresh_with_cache")
    @error_handler
    @required_account
    async def refresh_with_webcache(self):
        client: HSRClient = self.app.client
        self.notify("正在更新数据")
        await client.refresh_gacha_record("webcache")
        self.analyze_result = await client.view_analysis_results()
        self.notify("更新已完成")

    @work(exclusive=True)
    @on(SimpleButton.Pressed, "#refresh_with_url")
    @error_handler
    @required_account
    async def refresh_with_url(self):
        client: HSRClient = self.app.client
        self.notify("正在更新数据")
        await client.refresh_gacha_record("clipboard")
        self.analyze_result = await client.view_analysis_results()
        self.notify("更新已完成")

    async def view_record(self):
        client: HSRClient = self.app.client
        self.analyze_result = await client.view_analysis_results()

    @work(exclusive=True)
    @on(SimpleButton.Pressed, "#import")
    @error_handler
    @required_account
    async def import_srgf(self):
        client: HSRClient = self.app.client
        cnt, failed_list = await client.import_srgf_json()
        if cnt:
            self.notify(f"新增{cnt}条记录")
        else:
            self.notify("无数据可导入")
        if failed_list:
            self.notify("\n".join([f"文件{name }导入失败" for name in failed_list]))

    @work(exclusive=True)
    @on(SimpleButton.Pressed, "#export_execl")
    @error_handler
    @required_account
    async def export_to_execl(self):
        client: HSRClient = self.app.client
        await client.export_to_execl()
        self.notify(f"导出成功, 文件位于{client.user.gacha_record_xlsx_path.as_posix()}")

    @work(exclusive=True)
    @on(SimpleButton.Pressed, "#export_srgf")
    @error_handler
    @required_account
    async def export_to_srgf(self):
        client: HSRClient = self.app.client
        await client.export_to_srgf()
        self.notify(f"导出成功, 文件位于{client.user.srgf_path.as_posix()}")
