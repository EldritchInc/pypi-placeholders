"""Tests that the placeholders can reach nothing beyond the installed packages' metadata.

A placeholder is what someone installs by mistake, so an IT review should
find in it nothing that reaches a network, runs a program, or reads or
writes a file. The tests read each module's source and allow only the
imports the report needs.
"""

import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parents[1]

ALLOWED_IMPORTS = {
    "__future__",
    "collections.abc",
    "importlib.metadata",
    "importlib.util",
    "platform",
    "sys",
    "typing",
    "azathoth_team_placeholder",
    "eldritch_licensing_placeholder",
}
"""Every module a placeholder may import."""

FORBIDDEN_NAMES = {"open", "exec", "eval", "compile", "__import__", "input"}
"""Built-ins that would read, write or run what the report never needs."""


def sources() -> list[Path]:
    return sorted(PROJECT_ROOT.glob("*/src/**/*.py"))


def test_both_placeholders_are_read() -> None:
    assert [path.relative_to(PROJECT_ROOT).as_posix() for path in sources()] == [
        "azathoth-team/src/azathoth_team/__init__.py",
        "azathoth-team/src/azathoth_team_placeholder/__init__.py",
        "eldritch-licensing/src/eldritch_licensing/__init__.py",
        "eldritch-licensing/src/eldritch_licensing_placeholder/__init__.py",
    ]


@pytest.mark.parametrize("path", sources(), ids=lambda path: path.parent.name)
def test_a_placeholder_imports_only_what_the_report_needs(
    path: Path,
) -> None:
    imported: set[str] = set()

    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0, path
            imported.add(node.module or "")

    assert imported <= ALLOWED_IMPORTS, imported - ALLOWED_IMPORTS


@pytest.mark.parametrize("path", sources(), ids=lambda path: path.parent.name)
def test_a_placeholder_calls_nothing_that_reads_writes_or_runs(
    path: Path,
) -> None:
    called = {
        node.func.id
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert called.isdisjoint(FORBIDDEN_NAMES), called & FORBIDDEN_NAMES
