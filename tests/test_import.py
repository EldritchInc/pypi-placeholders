"""Tests that importing a held name fails, saying where the real package comes from."""

import importlib
import sys

import pytest

from azathoth_team_placeholder import WORK_WITH_US


@pytest.mark.parametrize(
    ("module", "product"),
    [("azathoth_team", "azathoth-team"), ("eldritch_licensing", "eldritch-licensing")],
)
def test_importing_the_held_package_raises_import_error(
    module: str,
    product: str,
) -> None:
    sys.modules.pop(module, None)

    with pytest.raises(ImportError) as caught:
        importlib.import_module(module)

    assert str(caught.value) == (
        f"{product} is not distributed on PyPI; the package installed under its name is "
        f"Eldritch, Inc.'s placeholder. Run `{product}` to see what is installed, or write "
        f"to us at {WORK_WITH_US}."
    )
    assert module not in sys.modules
