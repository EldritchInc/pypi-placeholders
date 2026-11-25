"""Tests for what each placeholder says when it is run.

The report names what is installed, says the product is not distributed
on PyPI, and says where to ask for it. It is built from versions it is
given, so the tests need no installed Azathoth.
"""

from types import ModuleType

import pytest

import azathoth_team_placeholder
import eldritch_licensing_placeholder
from azathoth_team_placeholder import (
    DISTRIBUTIONS,
    PRODUCTS,
    WORK_WITH_US,
    installed,
    report,
)

PLACEHOLDERS = (azathoth_team_placeholder, eldritch_licensing_placeholder)

VERSIONS = {
    "azathoth-ai": "1.6.0",
    "azathoth-mcp": None,
    "azathoth-ui": "1.6.0",
    "azathoth-team": "0.0.1",
    "eldritch-licensing": None,
}


def test_every_eldritch_distribution_is_reported_in_order() -> None:
    assert DISTRIBUTIONS == (
        "azathoth-ai",
        "azathoth-mcp",
        "azathoth-ui",
        "azathoth-team",
        "eldritch-licensing",
    )


def test_each_placeholder_reports_for_its_own_product() -> None:
    assert [placeholder.PRODUCT for placeholder in PLACEHOLDERS] == [
        "azathoth-team",
        "eldritch-licensing",
    ]
    assert set(PRODUCTS) == {"azathoth-team", "eldritch-licensing"}


def test_the_report_says_the_product_is_not_on_pypi_and_where_to_ask() -> None:
    text = report("azathoth-team", VERSIONS, python="3.13.1", system="macOS-15.1-arm64")

    assert text.startswith("azathoth-team is not distributed on PyPI.\n")
    assert PRODUCTS["azathoth-team"] in text
    assert f"\nTo get it, write to us at {WORK_WITH_US}\nand include the lines above.\n" in text
    assert WORK_WITH_US == "https://eldritchinc.com/workwithus/"


def test_the_report_lists_python_and_every_distribution_aligned() -> None:
    text = report("azathoth-team", VERSIONS, python="3.13.1", system="macOS-15.1-arm64")

    assert (
        "Installed here:\n"
        "  Python              3.13.1 (macOS-15.1-arm64)\n"
        "  azathoth-ai         1.6.0\n"
        "  azathoth-mcp        not installed\n"
        "  azathoth-ui         1.6.0\n"
        "  azathoth-team       0.0.1 (this placeholder)\n"
        "  eldritch-licensing  not installed\n"
    ) in text


def test_the_other_placeholder_is_named_as_one_when_installed() -> None:
    versions = {**VERSIONS, "eldritch-licensing": "0.0.1"}
    text = report(
        "azathoth-team",
        versions,
        python="3.13.1",
        system="Linux",
        placeholders={"azathoth-team", "eldritch-licensing"},
    )

    assert "  eldritch-licensing  0.0.1 (a placeholder)\n" in text


def test_the_report_says_how_to_remove_the_placeholder() -> None:
    text = report("eldritch-licensing", VERSIONS, python="3.13.1", system="Linux")

    assert text.endswith(
        "To remove this placeholder:\n  python -m pip uninstall eldritch-licensing\n"
    )


def test_a_product_that_is_not_held_is_refused() -> None:
    with pytest.raises(KeyError):
        report("cthulhu-ai", VERSIONS, python="3.13.1", system="Linux")


def test_installed_reads_each_distributions_version_here() -> None:
    found = installed()

    assert tuple(found) == DISTRIBUTIONS
    assert found["azathoth-team"] == "0.0.1"
    assert found["eldritch-licensing"] == "0.0.1"


@pytest.mark.parametrize("placeholder", PLACEHOLDERS)
def test_running_a_placeholder_prints_the_report_and_fails(
    placeholder: ModuleType,
    capsys: pytest.CaptureFixture[str],
) -> None:
    product: str = placeholder.PRODUCT

    assert placeholder.main(["init", "--anything"]) == 1

    out, err = capsys.readouterr()

    assert out.startswith(f"{product} is not distributed on PyPI.\n")
    assert f"  {product}" in out
    assert err == ""
