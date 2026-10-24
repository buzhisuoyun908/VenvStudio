"""
VenvStudio - Settings Common
Shared, dependency-free widgets/constants used by SettingsPage and its mixins.
Kept in its own module (no imports from settings_page.py or any mixin) to avoid
circular imports, since multiple mixins need these.
"""
from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import Qt


class NoScrollComboBox(QComboBox):
    """ComboBox that ignores mouse wheel events unless explicitly focused by click."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self._clicked = False

    def mousePressEvent(self, event):
        self._clicked = True
        super().mousePressEvent(event)

    def wheelEvent(self, event):
        if self._clicked and self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()

    def focusOutEvent(self, event):
        self._clicked = False
        super().focusOutEvent(event)


# Dil tanımları / Language names.
# Single source of truth: src/utils/i18n.py decides what a language is called
# and which codes exist, because the runtime translator needs the same table.
from src.utils.i18n import LANGUAGES  # noqa: E402,F401  (re-exported)
