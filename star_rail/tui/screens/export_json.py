from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen

from star_rail.tui.widgets import SimpleButton

__all__ = ["ExportJsonScreen"]


class ExportJsonScreen(ModalScreen[str]):
    BINDINGS = [("escape", "cancel", "cancel export json")]

    def compose(self) -> ComposeResult:
        with Vertical():
            yield SimpleButton("导出 SRGF", id="export_srgf")
            yield SimpleButton("导出 UIGF", id="export_uigf")
            yield SimpleButton("取消", id="cancel")

    @on(SimpleButton.Pressed, "#cancel")
    def action_cancel(self):
        self.app.pop_screen()

    @on(SimpleButton.Pressed, "#export_uigf")
    @on(SimpleButton.Pressed, "#export_srgf")
    def export_json(self, event: SimpleButton.Pressed):
        self.dismiss(event.button.id)
