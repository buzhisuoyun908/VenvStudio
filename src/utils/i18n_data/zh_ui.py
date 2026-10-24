"""Chinese UI text dictionary — aggregation point.

The dictionary is split by area so each file stays reviewable:

    zh_ui_core.py     main window, menus, environment dialogs, common words
    zh_ui_pages.py    settings pages, package manager, projects, launcher
    zh_ui_catalog.py  package / preset catalog descriptions (constants.py)
    zh_ui_learn.py    Learn page topics and cards

A missing module is skipped, so a partial checkout still works. The runtime
layer in src/utils/i18n.py imports ``UI_TEXT`` from here and treats it as
"English source text -> Simplified Chinese".
"""

from .zh_ui_core import UI_TEXT as _CORE

UI_TEXT = {}
UI_TEXT.update(_CORE)

try:
    from .zh_ui_pages import UI_TEXT as _PAGES
    UI_TEXT.update(_PAGES)
except ImportError:
    pass

try:
    from .zh_ui_catalog import UI_TEXT as _CATALOG
    UI_TEXT.update(_CATALOG)
except ImportError:
    pass

try:
    from .zh_ui_packages import UI_TEXT as _PACKAGES
    UI_TEXT.update(_PACKAGES)
except ImportError:
    pass

try:
    from .zh_ui_dialogs import UI_TEXT as _DIALOGS
    UI_TEXT.update(_DIALOGS)
except ImportError:
    pass

try:
    from .zh_ui_learn import UI_TEXT as _LEARN
    UI_TEXT.update(_LEARN)
except ImportError:
    pass
