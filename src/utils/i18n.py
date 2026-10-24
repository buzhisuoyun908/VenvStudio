"""
VenvStudio - Internationalization (i18n) System
Supports: en, tr, de, fr, es, pt, ru, zh, ja, ko, ar

Translation data lives in src/utils/i18n_data/<lang>.py (one dict per
language). This module keeps the public API (tr / set_language /
get_language) and assembles the combined TRANSLATIONS dict from them.

Two layers, on purpose
----------------------
1. ``tr(key)`` — key-based lookup, used by code that was written with i18n in
   mind (``tr("new_environment")``). Fast and unambiguous; the key never
   changes when the English copy is reworded.

2. ``render(text)`` — text-based lookup, used by the runtime layer in
   ``src/utils/i18n_qt.py``. Most of VenvStudio's widgets were written with
   literal English strings, and rewriting tens of thousands of lines to call
   ``tr()`` would have been a bigger risk than the feature is worth. Instead,
   already built widgets hand their English text to ``render()``, which looks
   it up in ``i18n_data/zh_ui*.py``. Untranslated text comes back unchanged, so
   coverage is always safe to grow.

``canonical()`` is the inverse of ``render()``: it maps a translated string
back to the English source it came from. That is what makes a *live* language
switch possible — every widget remembers its English source once, and a switch
just re-renders from it instead of rebuilding the window.
"""

import os as _os
import re as _re
import sys as _sys

from src.utils.i18n_data.en import TRANSLATIONS as _EN
from src.utils.i18n_data.tr import TRANSLATIONS as _TR
from src.utils.i18n_data.de import TRANSLATIONS as _DE
from src.utils.i18n_data.fr import TRANSLATIONS as _FR
from src.utils.i18n_data.es import TRANSLATIONS as _ES
from src.utils.i18n_data.pt import TRANSLATIONS as _PT
from src.utils.i18n_data.ru import TRANSLATIONS as _RU
from src.utils.i18n_data.zh import TRANSLATIONS as _ZH
from src.utils.i18n_data.ja import TRANSLATIONS as _JA
from src.utils.i18n_data.ko import TRANSLATIONS as _KO
from src.utils.i18n_data.ar import TRANSLATIONS as _AR
from src.utils.i18n_data.zh_ui import UI_TEXT as _UI_TEXT


TRANSLATIONS = {
    "en": _EN,
    "tr": _TR,
    "de": _DE,
    "fr": _FR,
    "es": _ES,
    "pt": _PT,
    "ru": _RU,
    "zh": _ZH,
    "ja": _JA,
    "ko": _KO,
    "ar": _AR,
}

#: Language code -> name in that language, as shown in the selector.
#: Order: English, Simplified Chinese, then the rest.
LANGUAGES = {
    "en": "English",
    "zh": "简体中文",
    "tr": "Türkçe",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "pt": "Português",
    "ru": "Русский",
    "ja": "日本語",
    "ko": "한국어",
    "ar": "العربية",
}

#: Languages written right-to-left. The Qt layer mirrors layouts for these.
RTL_LANGUAGES = frozenset({"ar"})

#: The language the UI text dictionary (zh_ui*) is written in.
_UI_TEXT_LANG = "zh"

_current_lang = "en"
_listeners = []


# ── Indexes built once at import ──────────────────────────────────────────────
_EN_VALUE_OF_KEY = {}    # english UI text -> key            (render)
_REV_KEY = {}            # lang -> {translated text: english} (canonical)
_REV_UI = {}             # chinese text -> english source     (canonical)
_TEMPLATES = []          # [(compiled regex, chinese template)] for "{n}" text

_PLACEHOLDER = _re.compile(r"\{(\w+)\}")


def _compile_template(english: str):
    """Turn 'Found {n} environments' into a regex that captures {n}."""
    parts = []
    pos = 0
    for m in _PLACEHOLDER.finditer(english):
        parts.append(_re.escape(english[pos:m.start()]))
        parts.append(r"(?P<%s>.+?)" % m.group(1))
        pos = m.end()
    parts.append(_re.escape(english[pos:]))
    try:
        return _re.compile("^" + "".join(parts) + "$", _re.DOTALL)
    except _re.error:
        return None


def _build_indexes():
    for key, en in _EN.items():
        if isinstance(en, str) and en:
            _EN_VALUE_OF_KEY.setdefault(en, key)

    for lang, table in TRANSLATIONS.items():
        rev = {}
        for key, value in table.items():
            en = _EN.get(key)
            if isinstance(value, str) and isinstance(en, str) and value:
                rev.setdefault(value, en)
        _REV_KEY[lang] = rev

    for en, zh in _UI_TEXT.items():
        if not isinstance(zh, str) or not isinstance(en, str):
            continue
        _REV_UI.setdefault(zh, en)
        if "{" in en:
            rx = _compile_template(en)
            if rx is not None:
                _TEMPLATES.append((rx, zh))


_build_indexes()


# ── Public API ────────────────────────────────────────────────────────────────
def normalize_code(code: str) -> str:
    """'zh_CN' / 'zh-Hans-CN' / 'ZH' -> 'zh'. Unknown codes fall back to 'en'."""
    if not code:
        return "en"
    code = str(code).replace("-", "_").split("_")[0].strip().lower()
    return code if code in TRANSLATIONS else "en"


def get_language() -> str:
    return _current_lang


def set_language(lang_code: str) -> str:
    """Switch the active language and notify every registered listener.

    Returns the code that actually took effect (normalized).
    """
    global _current_lang
    code = normalize_code(lang_code)
    changed = code != _current_lang
    _current_lang = code
    if changed:
        for cb in list(_listeners):
            try:
                cb(code)
            except Exception:
                # A broken listener must never break the switch itself.
                pass
    return code


def add_language_listener(callback) -> None:
    """Register ``callback(lang_code)`` to run after every language change."""
    if callback not in _listeners:
        _listeners.append(callback)


def remove_language_listener(callback) -> None:
    try:
        _listeners.remove(callback)
    except ValueError:
        pass


def tr(key: str) -> str:
    """Translate a key to the current language. Falls back to English."""
    lang_dict = TRANSLATIONS.get(_current_lang, TRANSLATIONS["en"])
    return lang_dict.get(key, TRANSLATIONS["en"].get(key, key))


def _fill(template: str, captured: dict) -> str:
    def _sub(m):
        return captured.get(m.group(1), m.group(0))
    return _PLACEHOLDER.sub(_sub, template)


def render(text):
    """Localize a piece of already-written English UI text.

    Returns the text unchanged when nothing matches, so callers never have to
    guard for missing translations. Non-strings are returned as-is.
    """
    if not isinstance(text, str) or not text:
        return text

    if _current_lang == _UI_TEXT_LANG:
        hit = _UI_TEXT.get(text)
        if hit is not None:
            return hit
        for rx, zh in _TEMPLATES:
            m = rx.match(text)
            if m is not None:
                return _fill(zh, m.groupdict())

    key = _EN_VALUE_OF_KEY.get(text)
    if key is not None:
        table = TRANSLATIONS.get(_current_lang) or TRANSLATIONS["en"]
        return table.get(key, text)
    return text


def canonical(text):
    """Map a translated string back to the English source it came from.

    Lets a language switch re-render text that was already translated —
    including strings produced by ``tr()``. The UI-text map is consulted in
    every language, because its values are Chinese regardless of which
    language is active (a widget may have been built while Chinese was on and
    be re-rendered after the user switched back to English).
    """
    if not isinstance(text, str) or not text:
        return text
    hit = _REV_UI.get(text)
    if hit is not None:
        return hit
    rev = _REV_KEY.get(_current_lang)
    if rev:
        hit = rev.get(text)
        if hit is not None:
            return hit
    return text


def tr_text(text):
    """Alias for :func:`render`, for code that reads better as a verb."""
    return render(text)


def system_language(default: str = "en") -> str:
    """Best-effort guess at the language of the user's OS.

    Used only on the very first start, when no language is saved yet — a
    Chinese Windows should open in Chinese without the user having to find
    the setting first.
    """
    for var in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        raw = _os.environ.get(var, "")
        if raw and raw.strip():
            return normalize_code(raw.split(".")[0])

    if _sys.platform == "win32":
        try:
            import ctypes

            langid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            table = {
                0x04: "zh", 0x09: "en", 0x1F: "tr", 0x07: "de", 0x0C: "fr",
                0x0A: "es", 0x16: "pt", 0x19: "ru", 0x11: "ja", 0x12: "ko",
                0x01: "ar",
            }
            code = table.get(langid & 0x3FF)
            if code:
                return code
        except Exception:
            pass

    if _sys.platform == "darwin":
        try:
            from Foundation import NSUserDefaults  # type: ignore

            langs = NSUserDefaults.standardUserDefaults().arrayForKey_("AppleLanguages")
            if langs:
                return normalize_code(str(langs[0]))
        except Exception:
            pass

    try:
        import locale

        code = normalize_code(locale.getlocale()[0] or "")
        if code:
            return code
    except Exception:
        pass

    return normalize_code(default)


def is_rtl(lang: str = "") -> bool:
    return (lang or _current_lang) in RTL_LANGUAGES


def coverage() -> dict:
    """How complete the current language is, as counts (tests/settings UI)."""
    total = len(_EN)
    table = TRANSLATIONS.get(_current_lang, {})
    translated = sum(1 for k in _EN if k in table)
    return {
        "keys_total": total,
        "keys_translated": translated,
        "ui_strings_total": len(_UI_TEXT),
        "language": _current_lang,
    }
