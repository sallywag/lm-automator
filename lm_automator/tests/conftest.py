import pathlib

import pytest

from lm_automator.layout_manager import LayoutManager
from lm_automator.common import DRIVER


@pytest.fixture(scope="class")
def login():
    layout_manager = LayoutManager(environment="dev", site="fox29")
    layout_manager.login(
        username="salvatore.rosa@foxnews.com", password="RewqFdsaVcxz1718!"
    )


@pytest.fixture(scope="class")
def visit_test_site():
    DRIVER.get(
        "file://"
        + str(pathlib.Path.cwd().joinpath("lm_automator", "tests", "test-site.html"))
    )


@pytest.fixture(scope="session", autouse=True)
def close_browser():
    yield
    DRIVER.quit()
