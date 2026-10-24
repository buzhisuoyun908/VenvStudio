"""Tests for the i18n layer — dictionary, lookup, live switch bookkeeping.

These are decision tests, not widget tests: the whole point of
``render()``/``canonical()`` is that untranslated text passes through
unchanged and translated text can be mapped back to its English source. If
either property breaks, a language switch either blanks the UI or doubles the
translation, and both are silent failures. So they are pinned here.

Qt-dependent behaviour (widget text actually changing) lives in
tests/test_i18n_qt.py, which skips itself when PySide6 is only a stub.
"""

import pytest

from src.utils import i18n
from src.utils.i18n_data.en import TRANSLATIONS as EN
from src.utils.i18n_data.zh import TRANSLATIONS as ZH
from src.utils.i18n_data.zh_ui import UI_TEXT


@pytest.fixture(autouse=True)
def _restore_language():
    """Every test starts and ends in English, whatever it does in between."""
    i18n.set_language("en")
    yield
    i18n.set_language("en")


# ── Keys ─────────────────────────────────────────────────────────────────────
def test_every_english_key_has_a_chinese_translation():
    missing = [k for k in EN if k not in ZH]
    assert not missing, f"zh.py is missing keys: {missing[:10]}"


def test_chinese_translations_are_not_empty():
    empty = [k for k, v in ZH.items() if not v.strip()]
    assert not empty, f"empty zh translations: {empty[:10]}"


def test_unknown_key_falls_back_to_the_key_itself():
    assert i18n.tr("this_key_does_not_exist") == "this_key_does_not_exist"


def test_tr_switches_language():
    i18n.set_language("zh")
    assert i18n.tr("delete") == "删除"
    i18n.set_language("en")
    assert i18n.tr("delete") == "Delete"


# ── render() ─────────────────────────────────────────────────────────────────
def test_render_translates_a_known_ui_string():
    i18n.set_language("zh")
    assert i18n.render("Rename Environment") == "重命名环境"


def test_render_leaves_unknown_text_alone():
    i18n.set_language("zh")
    text = "Some sentence nobody has translated yet"
    assert i18n.render(text) == text


def test_render_passes_non_strings_through():
    i18n.set_language("zh")
    assert i18n.render(None) is None
    assert i18n.render(42) == 42
    assert i18n.render("") == ""


def test_render_is_identity_in_english():
    """No dictionary entry may rewrite English text while English is active."""
    for text in ("Rename Environment", "Settings", "Packages"):
        assert i18n.render(text) == text


def test_render_uses_tr_keys_for_text_matches():
    """Text that equals an English tr() value is translated through tr()."""
    i18n.set_language("zh")
    assert i18n.render(EN["delete_environment"]) == ZH["delete_environment"]


# ── canonical() ──────────────────────────────────────────────────────────────
def test_canonical_maps_chinese_back_to_english():
    i18n.set_language("zh")
    assert i18n.canonical("重命名环境") == "Rename Environment"


def test_canonical_understands_tr_output():
    i18n.set_language("zh")
    assert i18n.canonical(i18n.tr("delete")) == "Delete"


def test_canonical_leaves_unknown_text_alone():
    i18n.set_language("zh")
    assert i18n.canonical("某个没有对应的中文") == "某个没有对应的中文"


def test_round_trip_survives_a_language_switch():
    """The property the widget layer relies on: render(canonical(x)) is stable.

    A widget that already shows Chinese must come back as the same Chinese
    after a switch to English and back, not as English, and not doubled.
    """
    source = "Rename Environment"
    i18n.set_language("zh")
    chinese = i18n.render(source)

    i18n.set_language("en")
    assert i18n.render(i18n.canonical(chinese)) == source

    i18n.set_language("zh")
    assert i18n.render(i18n.canonical(chinese)) == chinese


# ── Templates ────────────────────────────────────────────────────────────────
def test_template_captures_a_placeholder():
    rx = i18n._compile_template("Found {n} environments")
    assert rx is not None
    m = rx.match("Found 7 environments")
    assert m is not None and m.group("n") == "7"


def test_template_does_not_match_unrelated_text():
    rx = i18n._compile_template("Found {n} environments")
    assert rx.match("Found environments") is None


def test_template_fill_keeps_the_captured_value():
    assert i18n._fill("找到 {n} 个环境", {"n": "7"}) == "找到 7 个环境"


# ── Language registry ────────────────────────────────────────────────────────
@pytest.mark.parametrize("code,expected", [
    ("zh", "zh"), ("zh_CN", "zh"), ("zh-Hans-CN", "zh"), ("ZH", "zh"),
    ("en_US", "en"), ("", "en"), (None, "en"), ("klingon", "en"),
])
def test_normalize_code(code, expected):
    assert i18n.normalize_code(code) == expected


def test_set_language_returns_the_effective_code():
    assert i18n.set_language("zh_CN") == "zh"
    assert i18n.get_language() == "zh"


def test_listeners_fire_once_per_real_change():
    seen = []
    i18n.add_language_listener(seen.append)
    try:
        i18n.set_language("zh")
        i18n.set_language("zh")       # same language: no second call
        i18n.set_language("en")
    finally:
        i18n.remove_language_listener(seen.append)
    assert seen == ["zh", "en"]


def test_a_broken_listener_does_not_block_the_switch():
    def _boom(_code):
        raise RuntimeError("listener exploded")

    i18n.add_language_listener(_boom)
    try:
        assert i18n.set_language("zh") == "zh"
        assert i18n.get_language() == "zh"
    finally:
        i18n.remove_language_listener(_boom)


def test_every_registered_language_has_a_display_name():
    for code in i18n.TRANSLATIONS:
        assert i18n.LANGUAGES.get(code), f"no display name for {code}"


def test_system_language_is_a_supported_code():
    assert i18n.system_language() in i18n.TRANSLATIONS


def test_rtl_is_reported_for_arabic_only():
    assert i18n.is_rtl("ar")
    assert not i18n.is_rtl("zh")


# ── Dictionary hygiene ───────────────────────────────────────────────────────
def test_ui_dictionary_is_substantial():
    # Guards against a truncated or half-imported dictionary file: the whole
    # point of the text layer is coverage, and a silent import failure would
    # look exactly like "translations stopped working".
    assert len(UI_TEXT) > 1000


def test_ui_dictionary_keys_are_clean():
    problems = []
    for key, value in UI_TEXT.items():
        if not key or not key.strip():
            problems.append(repr(key))
        if key != key.rstrip() and not key.endswith("\n"):
            problems.append(f"trailing space: {key!r}")
        if not isinstance(value, str) or not value.strip():
            problems.append(f"empty value for {key!r}")
    assert not problems, problems[:10]


def test_coverage_counts_add_up():
    i18n.set_language("zh")
    stats = i18n.coverage()
    assert stats["keys_total"] == len(EN)
    assert stats["keys_translated"] == len([k for k in EN if k in ZH])
    assert stats["ui_strings_total"] == len(UI_TEXT)
