"""Tests for the two placeholder distributions' metadata and files.

Each holds a name Eldritch's private packages are installed under, at a
version below any they require, so pip never takes a placeholder for the
real package. The two share one report module, byte for byte.
"""

import re
import tomllib
from pathlib import Path
from typing import Any

import pytest

PROJECT_ROOT = Path(__file__).parents[1]

PROJECTS = {
    "azathoth-team": "azathoth_team",
    "eldritch-licensing": "eldritch_licensing",
}
"""Each held distribution, by the package it holds."""

LOWEST_REAL_RELEASE = (0, 1, 0)
"""The lowest release of either private package that anything requires."""


def project(
    name: str,
) -> dict[str, Any]:
    """Return the `[project]` table of one placeholder's `pyproject.toml`."""

    with (PROJECT_ROOT / name / "pyproject.toml").open("rb") as file:
        table: dict[str, Any] = tomllib.load(file)["project"]

    return table


def report_module(
    name: str,
) -> Path:
    return PROJECT_ROOT / name / "src" / f"{PROJECTS[name]}_placeholder" / "__init__.py"


@pytest.mark.parametrize("name", PROJECTS)
def test_each_placeholder_is_named_for_the_package_it_holds(
    name: str,
) -> None:
    assert project(name)["name"] == name


@pytest.mark.parametrize("name", PROJECTS)
def test_each_version_is_below_any_real_release(
    name: str,
) -> None:
    version = project(name)["version"]

    assert re.fullmatch(r"\d+\.\d+\.\d+", version) is not None
    assert tuple(int(part) for part in version.split(".")) < LOWEST_REAL_RELEASE


@pytest.mark.parametrize("name", PROJECTS)
def test_each_depends_on_nothing(
    name: str,
) -> None:
    assert project(name).get("dependencies", []) == []
    assert "optional-dependencies" not in project(name)


@pytest.mark.parametrize("name", PROJECTS)
def test_each_installs_the_command_its_product_would_and_no_plugin(
    name: str,
) -> None:
    assert project(name)["scripts"] == {name: f"{PROJECTS[name]}_placeholder:main"}
    assert "entry-points" not in project(name)


@pytest.mark.parametrize("name", PROJECTS)
def test_each_says_it_is_a_placeholder_and_inactive(
    name: str,
) -> None:
    assert project(name)["description"] == (
        f"Placeholder held by Eldritch, Inc.: {name} is not distributed on PyPI."
    )
    assert "Development Status :: 7 - Inactive" in project(name)["classifiers"]
    assert project(name)["urls"] == {
        "Homepage": "https://eldritchinc.com/workwithus/",
        "Repository": "https://github.com/EldritchInc/pypi-placeholders",
    }


@pytest.mark.parametrize("name", PROJECTS)
def test_each_page_on_pypi_says_where_the_package_comes_from(
    name: str,
) -> None:
    readme = " ".join((PROJECT_ROOT / name / "README.md").read_text(encoding="utf-8").split())

    assert project(name)["readme"] == "README.md"
    assert f"`{name}` is not distributed on PyPI." in readme
    assert "https://eldritchinc.com/workwithus/" in readme
    assert "reads nothing but the versions of Python packages installed" in readme


@pytest.mark.parametrize("name", PROJECTS)
def test_each_carries_the_repositorys_licence(
    name: str,
) -> None:
    root = (PROJECT_ROOT / "LICENSE").read_text(encoding="utf-8")

    assert root.startswith("MIT License\n")
    assert (PROJECT_ROOT / name / "LICENSE").read_text(encoding="utf-8") == root
    assert project(name)["license"] == "MIT"


def test_the_two_report_modules_are_one_module() -> None:
    first, second = (report_module(name).read_bytes() for name in PROJECTS)

    assert first == second
