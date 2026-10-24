"""
VenvStudio - Qt integration for the i18n runtime layer

Why this exists
---------------
The widgets in VenvStudio are built with literal English strings. Wrapping
every one of them in ``tr()`` would have touched tens of thousands of lines
for the same result, and each edit would have been a chance to break a
decision the tests cannot see. So the translation happens *after* the widget
exists:

    localize_widget(w)  ->  for every text property on w:
                              remember its English source once (_i18n_src_*)
                              set the translated text

Two properties make this safe:

* Unknown text is returned unchanged (``render()`` never invents anything),
  so a partially translated dictionary degrades to English, not to blanks.
* Each widget keeps its English source, so switching languages is a re-render
  from that source, not a second translation of already-translated text.

``install(app)`` hooks an application-wide event filter so widgets built
later — dialogs, menus, message boxes — are translated when they are shown,
which is the first moment their text is final.

Deliberately NOT translated automatically
-----------------------------------------
* Table/list *cells* and combo-box *items*: they carry data (env names,
  paths, package names, theme ids) and translating them would corrupt
  comparisons the code makes later.
* Text under a widget's own data model (QStandardItemModel) — same reason.
"""

from src.utils.i18n import (
    add_language_listener, canonical, is_rtl, render,
)

#: Widget properties translated in place: (getter, setter)
_TEXT_PROPS = (
    ("windowTitle", "setWindowTitle"),
    ("toolTip", "setToolTip"),
    ("statusTip", "setStatusTip"),
    ("text", "setText"),
    ("title", "setTitle"),
    ("placeholderText", "setPlaceholderText"),
)

#: Attribute used to remember the English source of a text property.
_SRC_ATTR = "_i18n_src_%s"

#: Guard so a widget subtree is not walked twice for the same language.
_STAMP_ATTR = "_i18n_stamp"
_stamp = [0]

#: Keep the event filter object alive for the lifetime of the application.
_filter_ref = []


def _translate_prop(obj, getter: str, setter: str) -> None:
    get = getattr(obj, getter, None)
    put = getattr(obj, setter, None)
    if get is None or put is None:
        return
    try:
        current = get()
    except Exception:
        return
    if not isinstance(current, str) or not current:
        return

    attr = _SRC_ATTR % getter
    try:
        source = getattr(obj, attr, None)
    except Exception:
        source = None
    if source is None:
        # First sight of this text: keep the English original as the source.
        source = canonical(current)
        try:
            setattr(obj, attr, source)
        except Exception:
            return

    translated = render(source)
    if translated and translated != current:
        try:
            put(translated)
        except Exception:
            pass


def _translate_menu_actions(menu, depth: int = 0) -> None:
    """Actions live in a menu, not in its widget tree."""
    if depth > 6:
        return
    try:
        actions = menu.actions()
    except Exception:
        return
    for act in actions:
        _translate_prop(act, "text", "setText")
        _translate_prop(act, "toolTip", "setToolTip")
        _translate_prop(act, "statusTip", "setStatusTip")
        try:
            sub = act.menu()
        except Exception:
            sub = None
        if sub is not None:
            _translate_menu_actions(sub, depth + 1)


def _translate_tabs(widget) -> None:
    """QTabWidget / QTabBar tab labels."""
    count = getattr(widget, "count", None)
    tab_text = getattr(widget, "tabText", None)
    set_tab_text = getattr(widget, "setTabText", None)
    if not (callable(count) and callable(tab_text) and callable(set_tab_text)):
        return
    try:
        n = count()
    except Exception:
        return
    if not isinstance(n, int) or n <= 0 or n > 200:
        return
    src_list = getattr(widget, "_i18n_tab_src", None)
    if src_list is None or len(src_list) != n:
        src_list = []
        for i in range(n):
            try:
                src_list.append(canonical(tab_text(i)))
            except Exception:
                src_list.append("")
        try:
            widget._i18n_tab_src = src_list
        except Exception:
            return
    for i in range(n):
        try:
            translated = render(src_list[i])
            if translated and translated != tab_text(i):
                set_tab_text(i, translated)
        except Exception:
            continue


def _translate_headers(widget) -> None:
    """QTableWidget / QTreeWidget column headers."""
    width = getattr(widget, "columnCount", None)
    if not (callable(width) and callable(getattr(widget, "horizontalHeaderItem", None))):
        return
    try:
        n = width()
    except Exception:
        return
    if not isinstance(n, int) or n <= 0 or n > 64:
        return
    for i in range(n):
        try:
            item = widget.horizontalHeaderItem(i)
        except Exception:
            continue
        if item is None:
            continue
        _translate_prop(item, "text", "setText")

    try:                                  # QTreeWidget
        header = widget.headerItem()
    except Exception:
        header = None
    if header is not None:
        _translate_prop(header, "text", "setText")


def localize_widget(widget) -> None:
    """Translate every text property of a single widget/action."""
    # A widget whose visible text is *composed* (icon + padding + word, like
    # SidebarButton) cannot be looked up in the dictionary as a finished
    # string. Such widgets expose _i18n_rebuild and re-compose from their key.
    # Its own ``text`` is then off limits for the generic pass below: that pass
    # remembers the first text it sees as the English source, and for a rebuilt
    # widget the first text it sees is already translated — it would translate
    # the translation back and undo the rebuild.
    rebuild = getattr(widget, "_i18n_rebuild", None)
    rebuilt = False
    if callable(rebuild):
        try:
            rebuild()
            rebuilt = True
        except Exception:
            pass

    for getter, setter in _TEXT_PROPS:
        if rebuilt and getter == "text":
            continue
        _translate_prop(widget, getter, setter)
    _translate_tabs(widget)
    _translate_headers(widget)
    _translate_menu_actions(widget)


def localize_tree(root) -> None:
    """Translate *root* and everything below it (depth-first)."""
    if root is None:
        return
    stamp = _stamp[0]
    try:
        if getattr(root, _STAMP_ATTR, None) == stamp:
            return
        setattr(root, _STAMP_ATTR, stamp)
    except Exception:
        pass

    localize_widget(root)
    try:
        children = root.children()
    except Exception:
        return
    for child in children or ():
        localize_tree(child)


def retranslate_all() -> int:
    """Re-render every live widget from its remembered English source.

    Called after a language switch. Returns the number of top-level windows
    visited, which the settings page logs.
    """
    _stamp[0] += 1
    try:
        from PySide6.QtWidgets import QApplication

        app = QApplication.instance()
    except Exception:
        return 0
    if app is None:
        return 0

    count = 0
    for w in app.allWidgets():
        try:
            localize_widget(w)
        except Exception:
            continue
        if w.isWindow():
            count += 1
    for w in app.topLevelWidgets():
        try:
            localize_tree(w)
        except Exception:
            continue
    return count


def apply_layout_direction(app=None) -> None:
    """Mirror the layout for right-to-left languages (Arabic)."""
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import QApplication

        app = app or QApplication.instance()
        if app is None:
            return
        app.setLayoutDirection(
            Qt.RightToLeft if is_rtl() else Qt.LeftToRight)
    except Exception:
        pass


def install(app=None) -> bool:
    """Install the application-wide "translate on show" filter.

    Returns True when the filter was installed. Safe to call twice.
    """
    if _filter_ref:
        return True
    try:
        from PySide6.QtCore import QEvent, QObject
        from PySide6.QtWidgets import QApplication

        app = app or QApplication.instance()
        if app is None:
            return False

        class _I18nEventFilter(QObject):
            """Translates widgets at the moment they become visible."""

            def eventFilter(self, obj, event):     # noqa: N802 (Qt name)
                try:
                    etype = event.type()
                    if etype == QEvent.Show:
                        localize_tree(obj)
                    elif etype == QEvent.Polish:
                        localize_widget(obj)
                except Exception:
                    pass
                return False

        filt = _I18nEventFilter(app)
        app.installEventFilter(filt)
        _filter_ref.append(filt)
        add_language_listener(lambda _code: retranslate_all())
        apply_layout_direction(app)
        return True
    except Exception:
        # Translation is a nicety; never let it stop the app from starting.
        return False
