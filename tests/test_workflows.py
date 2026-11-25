"""Tests for how the placeholders are checked and published.

Each placeholder has a release workflow of its own, since PyPI trusts one
workflow file to publish one new project. A tag naming the product and its
version builds that product's wheel and nothing else, runs it, and
publishes it to PyPI with trusted publishing; no token is kept anywhere.
The tests read the workflows as text, as GitHub runs them.
"""

import re
import tomllib
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parents[1]

WORKFLOWS = PROJECT_ROOT / ".github" / "workflows"

PRODUCTS = ("azathoth-team", "eldritch-licensing")


def release(
    product: str,
) -> str:
    return (WORKFLOWS / f"release-{product}.yml").read_text(encoding="utf-8")


def ci() -> str:
    return (WORKFLOWS / "ci.yml").read_text(encoding="utf-8")


def job(
    text: str,
    name: str,
) -> str:
    """Return the text of one job of a workflow."""

    body = text.split("\njobs:\n", 1)[1]
    (found,) = [
        each
        for each in re.split(r"\n(?=  [a-z-]+:\n)", "\n" + body)
        if each.startswith(f"  {name}:\n")
    ]

    return found


def version(
    product: str,
) -> str:
    with (PROJECT_ROOT / product / "pyproject.toml").open("rb") as file:
        declared: str = tomllib.load(file)["project"]["version"]

    return declared


def test_the_repository_runs_ci_and_one_release_for_each_placeholder() -> None:
    assert sorted(path.name for path in WORKFLOWS.glob("*.y*ml")) == [
        "ci.yml",
        "release-azathoth-team.yml",
        "release-eldritch-licensing.yml",
    ]


def test_the_two_releases_are_one_workflow_for_two_products() -> None:
    first, second = PRODUCTS

    assert release(first).replace(first, second).replace(
        first.replace("-", "_"), second.replace("-", "_")
    ) == release(second)


@pytest.mark.parametrize("product", PRODUCTS)
def test_only_a_tag_naming_the_product_runs_its_release(
    product: str,
) -> None:
    assert f'\non:\n  push:\n    tags:\n      - "{product}-v*"\n\n' in release(product)
    assert "workflow_dispatch" not in release(product)
    assert "pull_request" not in release(product)
    assert "branches:" not in release(product)


@pytest.mark.parametrize("product", PRODUCTS)
def test_the_tag_must_name_the_declared_version(
    product: str,
) -> None:
    build = job(release(product), "build")

    assert f"open('{product}/pyproject.toml', 'rb')" in build
    assert f'if [ "${{GITHUB_REF_NAME}}" != "{product}-v${{version}}" ]; then' in build


@pytest.mark.parametrize("product", PRODUCTS)
def test_the_release_builds_only_its_own_wheel(
    product: str,
) -> None:
    build = job(release(product), "build")
    (other,) = [each for each in PRODUCTS if each != product]

    assert f"python -m build --wheel --outdir dist {product}\n" in build
    assert f'test "$(ls dist)" = "{product.replace("-", "_")}-${{VERSION}}-py3-none-any.whl"' in (
        build
    )
    assert f"--outdir dist {other}" not in release(product)


@pytest.mark.parametrize("product", PRODUCTS)
def test_the_release_tests_installs_the_wheel_alone_and_runs_it(
    product: str,
) -> None:
    build = job(release(product), "build")
    module = product.replace("-", "_")

    assert "run: make install\n" in build
    assert "run: python -m pytest\n" in build
    assert "working-directory: ${{ runner.temp }}" in build
    assert (
        '"${RUNNER_TEMP}/release-check/bin/python" -m pip install "${GITHUB_WORKSPACE}"/dist/*.whl'
    ) in build
    assert f'output="$("${{RUNNER_TEMP}}/release-check/bin/{product}")" || status=$?' in build
    assert 'test "${status}" -eq 1' in build
    assert f'test "${{output%%$\'\\n\'*}}" = "{product} is not distributed on PyPI."' in build
    assert f'if "${{RUNNER_TEMP}}/release-check/bin/python" -c "import {module}"; then' in build


@pytest.mark.parametrize("product", PRODUCTS)
def test_only_the_publish_job_may_ask_pypi_to_trust_it(
    product: str,
) -> None:
    text = release(product)
    publish = job(text, "publish")

    assert "\npermissions:\n  contents: read\n\n" in text
    assert text.count("id-token: write") == 1
    assert "    permissions:\n      id-token: write\n" in publish
    assert (
        f"    environment:\n      name: pypi\n      url: https://pypi.org/p/{product}\n"
    ) in publish
    assert "    needs: build\n" in publish
    assert "uses: pypa/gh-action-pypi-publish@release/v1\n" in publish


@pytest.mark.parametrize("product", PRODUCTS)
def test_the_release_keeps_no_token_and_never_names_testpypi(
    product: str,
) -> None:
    assert "secrets." not in release(product)
    assert "password" not in release(product)
    assert "test.pypi.org" not in release(product)


def test_ci_checks_quality_and_tests_where_people_install_by_mistake() -> None:
    quality = job(ci(), "quality")
    tests = job(ci(), "tests")
    matrix = tests.split("\n        os:\n", 1)[1].split("\n        python-version:", 1)[0]

    assert "run: python -m ruff check .\n" in quality
    assert "run: python -m ruff format --check .\n" in quality
    assert "run: python -m mypy azathoth-team/src eldritch-licensing/src tests\n" in quality
    assert [line.strip() for line in matrix.splitlines()] == [
        "- ubuntu-latest",
        "- macos-latest",
        "- windows-latest",
    ]
    assert "run: python -m pytest\n" in tests
    assert "id-token" not in ci()
    assert "\npermissions:\n  contents: read\n\n" in ci()


@pytest.mark.parametrize("product", PRODUCTS)
def test_the_readme_says_how_each_placeholder_is_released(
    product: str,
) -> None:
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    assert f"git tag {product}-v{version(product)}\n" in readme
    assert f"git push origin {product}-v{version(product)}\n" in readme
    assert f"`release-{product}.yml`" in readme
