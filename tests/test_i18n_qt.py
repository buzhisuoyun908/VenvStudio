"""Widget-level tests for the i18n runtime layer.

Skipped automatically when PySide6 is only the import stub that conftest.py
installs: those tests can prove a module imports, not that a label changes
text. In CI the PySide6 install is optional, so this file must stay green
either way.
"""

import os
import sys

import pytest

pytest.importorskip("PySide6")

import PySide6  # noqa: E402

if getattr(PySide6, "__spec__", None) is None:      # conftest's stub module
    pytest.skip("PySide6 is stubbed in this environment", allow_module_level=True)

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import (  # noqa: E402
    QApplication, QCheckBox, QGroupBox, QLabel, QLineEdit, QMenu, QPushButton,
    QTabWidget, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout,
)

from src.utils import i18n  # noqa: E402
from src.utils import i18n_qt  # noqa: E402


@pytest.fixture(scope="module")
def app():
    app = QApplication.instance() or QApplication(sys.argv)
    i18n_qt.install(app)
    yield app


@pytest.fixture(autouse=True)
def _english():
    i18n.set_language("en")
    yield
    i18n.set_language("en")


def _build():
    """A window with one of every text-bearing widget the layer handles."""
    w = QWidget()
    w.setWindowTitle("Environment Settings")
    lay = QVBoxLayout(w)
    label = QLabel("This environment has no packages installed yet.")
    button = QPushButton("Delete")
    check = QCheckBox("Upgrade pip after creation")
    group = QGroupBox("Options")
    tabs = QTabWidget()
    tabs.addTab(QWidget(), "Installed")
    tabs.addTab(QWidget(), "Catalog")
    table = QTableWidget(1, 2)
    table.setHorizontalHeaderItem(0, QTableWidgetItem("Package"))
    table.setHorizontalHeaderItem(1, QTableWidgetItem("Size"))
    line = QLineEdit()
    line.setPlaceholderText("Filter by package name…")
    menu = QMenu(w)
    menu.addAction("Conflict Manager")
    for widget in (label, button, check, group, tabs, table, line):
        lay.addWidget(widget)
    return w, dict(label=label, button=button, check=check, group=group,
                   tabs=tabs, table=table, line=line, menu=menu)


def test_widgets_are_translated_on_show(app):
    w, parts = _build()
    i18n.set_language("zh")
    w.show()
    app.processEvents()

    assert w.windowTitle() == "环境设置"
    assert parts["label"].text() == "该环境还没有安装任何包。"
    assert parts["button"].text() == "删除"
    assert parts["check"].text() == "创建后升级 pip"
    assert parts["group"].title() == "选项"
    assert parts["tabs"].tabText(0) == "已安装"
    assert parts["line"].placeholderText() == "按包名筛选…"
    assert parts["table"].horizontalHeaderItem(0).text() == "包"
    w.close()


def test_switching_back_restores_english(app):
    w, parts = _build()
    i18n.set_language("zh")
    w.show()
    app.processEvents()
    assert parts["button"].text() == "删除"

    i18n.set_language("en")          # listener -> retranslate_all
    app.processEvents()
    assert parts["button"].text() == "Delete"
    assert parts["label"].text() == "This environment has no packages installed yet."
    w.close()


def test_switching_twice_does_not_double_translate(app):
    w, parts = _build()
    for _ in range(3):
        i18n.set_language("zh")
        i18n.set_language("en")
    i18n.set_language("zh")
    w.show()
    app.processEvents()
    assert parts["button"].text() == "删除"
    assert parts["label"].text() == "该环境还没有安装任何包。"
    w.close()


def test_untranslated_text_is_left_alone(app):
    w = QWidget()
    label = QLabel("a string nobody translated 42")
    w.setWindowTitle("untouched title")
    i18n.set_language("zh")
    w.show()
    app.processEvents()
    assert label.text() == "a string nobody translated 42"
    assert w.windowTitle() == "untouched title"
    w.close()


def test_data_cells_are_not_translated(app):
    """Table cells carry data, not labels — translating them corrupts it."""
    w, parts = _build()
    parts["table"].setItem(0, 0, QTableWidgetItem("numpy"))
    i18n.set_language("zh")
    w.show()
    app.processEvents()
    assert parts["table"].item(0, 0).text() == "numpy"
    w.close()


def test_composed_button_rebuilds_from_its_key(app):
    """Sidebar labels are icon + spaces + word; the word must follow the switch."""
    from src.gui.widgets import SidebarButton

    btn = SidebarButton(i18n.tr("learn"), "📚", label_key="learn")
    i18n.set_language("zh")
    btn.show()
    app.processEvents()
    assert "学习" in btn.text()

    i18n.set_language("en")
    app.processEvents()
    assert "Learn" in btn.text()
    assert "学习" not in btn.text()
    btn.close()
