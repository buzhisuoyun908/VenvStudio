"""VenvStudio - Shared GUI Widgets
Small reusable widget/delegate classes used across multiple GUI modules
(moved from main_window.py).
"""
from PySide6.QtWidgets import QStyledItemDelegate, QPushButton
from PySide6.QtCore import Qt


class PathElideMiddleDelegate(QStyledItemDelegate):
    """
    Renders a table cell's text with middle-elision (e.g. ``C:\\Users\\…\\pppp-py3.13``)
    instead of the default right-elision Qt applies to QTableWidgetItem.

    Used for the Path column of the environment table where Poetry / pipx
    paths are long and the meaningful part (env name) is at the end, while
    the drive letter / Linux root at the start is also useful for context.
    The full path is preserved in the item's tooltip and accessible via
    ``item.toolTip()`` / ``item.text()`` regardless of how it's drawn.
    """
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        # Replace the text with a middle-elided version so Qt's normal
        # painter draws bold/foreground/selection like every other column.
        text = option.text
        if not text:
            return
        # Reserve a small margin (matches the QSS ::item padding 8px 12px)
        # so the ellipsis doesn't kiss the cell border.
        avail = max(0, option.rect.width() - 24)
        if avail <= 0:
            return
        option.text = option.fontMetrics.elidedText(text, Qt.ElideMiddle, avail)
        option.textElideMode = Qt.ElideMiddle


def _sidebar_display(text: str, icon_text: str = "") -> str:
    return f"  {icon_text}  {text}" if icon_text else f"  {text}"


class SidebarButton(QPushButton):
    """Custom sidebar navigation button.

    ``label_key`` is optional and, when given, is an i18n key rather than
    literal text. The button then rebuilds its own label whenever the language
    changes: the visible string is a composition (padding + emoji + word), so
    the runtime text layer cannot look it up in the dictionary — it has to be
    re-composed from the key instead.
    """

    def __init__(self, text, icon_text="", parent=None, label_key=None):
        super().__init__(_sidebar_display(text, icon_text), parent)
        self._sidebar_icon = icon_text
        self._sidebar_key = label_key
        self.setCheckable(True)
        self.setFixedHeight(44)
        self.setCursor(Qt.PointingHandCursor)
        if label_key:
            self._i18n_rebuild = self._rebuild_sidebar_label

    def _rebuild_sidebar_label(self):
        from src.utils.i18n import tr

        self.setText(_sidebar_display(tr(self._sidebar_key), self._sidebar_icon))





