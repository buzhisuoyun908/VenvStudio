"""Extract user-facing UI strings from VenvStudio's sources.

The translation dictionary (src/utils/i18n_data/zh_ui.py) maps English UI
text to Chinese. Hand-maintaining the list of "what counts as UI text" is
error-prone, so this tool walks the AST and collects literals that are
actually handed to the UI:

    QLabel("Text")            → constructor argument
    btn.setText("Text")       → setter call
    QMessageBox.warning(self, "Title", "Body")
    tabs.addTab(w, "Text")    → tab label
    combo.addItem("Text")     → item label

Run it to see which strings are missing from the Chinese dictionary:

    python tools/i18n_extract.py                # summary + counts
    python tools/i18n_extract.py --json out.json # machine-readable dump
    python tools/i18n_extract.py --missing      # only untranslated strings

It is a development tool only — nothing at runtime imports it.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

# ── Calls whose positional argument is UI text ────────────────────────────────
# name → indexes of positional args that hold UI text.
CONSTRUCTORS = {
    "QLabel": (0,),
    "QPushButton": (0,),
    "QCheckBox": (0,),
    "QRadioButton": (0,),
    "QToolButton": (0,),
    "QGroupBox": (0,),
    "QCommandLinkButton": (0,),
    "QListWidgetItem": (0,),
    "QTreeWidgetItem": (0,),
    "QTableWidgetItem": (0,),
    "QAction": (0, 1),          # QAction(text, parent) / QAction(icon, text, parent)
    "QMenu": (0,),
    "QDialog": (1,),            # QDialog(parent, title) is rare; set below
    "QTabWidget": (),
    "QLineEdit": (1,),          # QLineEdit(text, parent)
}

SETTERS = {
    "setText", "setTitle", "setToolTip", "setStatusTip", "setWindowTitle",
    "setPlaceholderText", "setTabText", "setInfoText", "setLabelText",
    "setDetailedText", "setWindowIconText", "setToolTipText",
}

# name → indexes of positional args that are text (rest are parents etc.)
MULTI_ARG = {
    "addTab": (1,),
    "insertTab": (2,),
    "addItem": (0,),
    "addItems": (0,),
    "addAction": (0,),
    "addMenu": (0,),
    "addRow": (1,),
    "addButton": (0,),
    "setHeaderLabels": (0,),
    "setHorizontalHeaderLabels": (0,),
    # QMessageBox / QInputDialog statics: (parent, title, text, ...)
    "information": (1, 2),
    "warning": (1, 2),
    "critical": (1, 2),
    "question": (1, 2),
    "getText": (1, 2),
    "getItem": (1, 2),
    "getInt": (1, 2),
    "getDouble": (1, 2),
}

# Subscript keys in data tables that hold human-readable copy.
DESC_KEYS = {"desc", "description", "label", "title", "hint", "help"}

_ASCII_WORD = re.compile(r"[A-Za-z]{2,}")
_SNAKE = re.compile(r"^[a-z0-9_\-\./ ]+$")
_NOT_TEXT = re.compile(r"^(https?://|www\.|--|#|\\|/|[A-Za-z]:\\)")


def _is_ui_text(s: str) -> bool:
    if not isinstance(s, str):
        return False
    s = s.strip()
    if len(s) < 2 or len(s) > 2000:
        return False
    if not _ASCII_WORD.search(s):
        return False
    if _NOT_TEXT.match(s):
        return False
    if _SNAKE.match(s):             # pure lowercase tokens / paths / commands
        return False
    if s.startswith("{") or s.endswith("}"):
        return False
    return True


def _literals(node) -> list[str]:
    """String constants inside an expression (f-strings contribute pieces)."""
    out = []
    for sub in ast.walk(node):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            out.append(sub.value)
        elif isinstance(sub, ast.JoinedStr):
            for piece in sub.values:
                if isinstance(piece, ast.Constant) and isinstance(piece.value, str):
                    out.append(piece.value)
    return out


def scan_file(path: Path) -> list[tuple[str, int, str]]:
    """Return [(text, lineno, api)] for UI strings found in *path*."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return []
    found: list[tuple[str, int, str]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = getattr(fn, "attr", None) or getattr(fn, "id", None)
        if not name:
            continue

        if name in CONSTRUCTORS:
            for idx in CONSTRUCTORS[name]:
                if idx < len(node.args):
                    for s in _literals(node.args[idx]):
                        if _is_ui_text(s):
                            found.append((s, node.lineno, name))

        if name in SETTERS and node.args:
            for s in _literals(node.args[0]):
                if _is_ui_text(s):
                    found.append((s, node.lineno, name))

        if name in MULTI_ARG:
            for idx in MULTI_ARG[name]:
                if idx < len(node.args):
                    node_arg = node.args[idx]
                    # addItems(["a", "b"]) — a list of strings
                    if isinstance(node_arg, (ast.List, ast.Tuple)):
                        for elt in node_arg.elts:
                            for s in _literals(elt):
                                if _is_ui_text(s):
                                    found.append((s, node.lineno, name))
                    else:
                        for s in _literals(node_arg):
                            if _is_ui_text(s):
                                found.append((s, node.lineno, name))

        # data tables: {"desc": "..."} / {"title": "..."}
        if isinstance(fn, ast.Attribute) and name in ("get", "set"):
            pass

    # dict literals with descriptive keys
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and k.value in DESC_KEYS:
                    for s in _literals(v):
                        if _is_ui_text(s):
                            found.append((s, node.lineno, f"dict[{k.value}]"))
    return found


def load_dictionary() -> dict[str, str]:
    sys.path.insert(0, str(ROOT))
    from src.utils.i18n_data.zh_ui import UI_TEXT  # type: ignore
    return UI_TEXT


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write full inventory to this file")
    ap.add_argument("--missing", action="store_true", help="only list missing")
    ap.add_argument("--limit", type=int, default=0, help="max lines to print")
    args = ap.parse_args()

    per_file: dict[str, list[tuple[str, int, str]]] = defaultdict(list)
    for path in sorted(SRC.rglob("*.py")):
        if "i18n_data" in path.parts:
            continue
        hits = scan_file(path)
        if hits:
            per_file[str(path.relative_to(ROOT)).replace(os.sep, "/")] = hits

    all_texts: dict[str, list[str]] = {}
    for f, hits in per_file.items():
        for text, line, api in hits:
            all_texts.setdefault(text, []).append(f"{f}:{line}")

    try:
        dictionary = load_dictionary()
    except Exception as exc:               # dictionary not written yet
        print(f"! could not load zh_ui.py: {exc}", file=sys.stderr)
        dictionary = {}

    missing = {t: v for t, v in all_texts.items() if t not in dictionary}
    print(f"files scanned : {len(per_file)}")
    print(f"unique strings: {len(all_texts)}")
    print(f"translated    : {len(all_texts) - len(missing)}")
    print(f"missing       : {len(missing)}")
    print()
    for f, hits in sorted(per_file.items(), key=lambda kv: -len(kv[1]))[:15]:
        print(f"  {len(hits):5d}  {f}")

    if args.json:
        Path(args.json).write_text(
            json.dumps(all_texts, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nwrote {args.json}")

    if args.missing:
        print()
        rows = sorted(missing)
        if args.limit:
            rows = rows[: args.limit]
        for t in rows:
            print(f"{t!r:>70}   {missing[t][0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
