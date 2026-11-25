"""A placeholder for one of Eldritch, Inc.'s private packages, which are not on PyPI.

Run under the product's name, it says what Azathoth packages are installed
here and where the product comes from. It reads nothing but the versions
of installed Python packages: it reaches no network, runs no program, and
reads and writes no file of its own.

This module is the same, byte for byte, in every placeholder; each takes
its product from its own package's name.
"""

import importlib.util
import platform
import sys
from collections.abc import Collection, Mapping, Sequence
from importlib.metadata import PackageNotFoundError, version

__all__ = [
    "DISTRIBUTIONS",
    "PRODUCT",
    "PRODUCTS",
    "WORK_WITH_US",
    "import_message",
    "installed",
    "installed_placeholders",
    "main",
    "report",
]

WORK_WITH_US = "https://eldritchinc.com/workwithus/"
"""Where to ask Eldritch, Inc. for a private package."""

DISTRIBUTIONS = (
    "azathoth-ai",
    "azathoth-mcp",
    "azathoth-ui",
    "azathoth-team",
    "eldritch-licensing",
)
"""Every distribution of Azathoth's, in the order the report lists them."""

PRODUCTS = {
    "azathoth-team": (
        "azathoth-team is the team tier of Azathoth: each person on a remote has an\n"
        "identity, roles, tokens and single sign-on of their own, and an audit\n"
        "records what each did. Eldritch, Inc. licenses it to teams."
    ),
    "eldritch-licensing": (
        "eldritch-licensing checks the licence an Azathoth remote with azathoth-team\n"
        "runs under. It comes with azathoth-team, which Eldritch, Inc. licenses to\n"
        "teams."
    ),
}
"""Each private product a placeholder holds the name of, and what it is."""

PRODUCT = __name__.removesuffix("_placeholder").replace("_", "-")
"""The product this placeholder holds the name of."""


def import_message(
    product: str,
) -> str:
    """Return what importing the held package says."""

    return (
        f"{product} is not distributed on PyPI; the package installed under its name is "
        f"Eldritch, Inc.'s placeholder. Run `{product}` to see what is installed, or write "
        f"to us at {WORK_WITH_US}."
    )


def installed() -> dict[str, str | None]:
    """Return the version of each of Azathoth's distributions installed here, or None."""

    found: dict[str, str | None] = {}

    for distribution in DISTRIBUTIONS:
        try:
            found[distribution] = version(distribution)
        except PackageNotFoundError:
            found[distribution] = None

    return found


def installed_placeholders() -> set[str]:
    """Return each product whose installed package is a placeholder."""

    return {
        product
        for product in PRODUCTS
        if importlib.util.find_spec(f"{product.replace('-', '_')}_placeholder") is not None
    }


def report(
    product: str,
    versions: Mapping[str, str | None],
    *,
    python: str,
    system: str,
    placeholders: Collection[str] = (),
) -> str:
    """Return what a placeholder says, for the versions installed."""

    about = PRODUCTS[product]
    width = max(len(name) for name in ("Python", *DISTRIBUTIONS)) + 2
    lines = [f"  {'Python':<{width}}{python} ({system})"]

    for distribution in DISTRIBUTIONS:
        found = versions.get(distribution)

        if found is None:
            shown = "not installed"
        elif distribution == product:
            shown = f"{found} (this placeholder)"
        elif distribution in placeholders:
            shown = f"{found} (a placeholder)"
        else:
            shown = found

        lines.append(f"  {distribution:<{width}}{shown}")

    listed = "\n".join(lines)

    return (
        f"{product} is not distributed on PyPI.\n"
        "\n"
        f"This package holds its name for Eldritch, Inc., so that nothing else can be\n"
        f"installed under it. It installed none of {product}'s code.\n"
        "\n"
        "Installed here:\n"
        f"{listed}\n"
        "\n"
        f"{about}\n"
        f"To get it, write to us at {WORK_WITH_US}\n"
        "and include the lines above.\n"
        "\n"
        "To remove this placeholder:\n"
        f"  python -m pip uninstall {product}\n"
    )


def main(
    argv: Sequence[str] | None = None,
) -> int:
    """Print the report, whatever the command was given, and fail, so a script stops here."""

    del argv
    sys.stdout.write(
        report(
            PRODUCT,
            installed(),
            python=platform.python_version(),
            system=platform.platform(terse=True),
            placeholders=installed_placeholders(),
        )
    )

    return 1
