import pytest

from lm_automator.page import Page
from lm_automator.common import DRIVER


@pytest.mark.usefixtures("login")
class TestPage:

    def test_visit_method_opens_correct_page(self):
        Page.visit("category")
        assert DRIVER.current_url == "https://dev-layout-cms.fox29.com/category"

    def test_select_layout_method_opens_correct_layout(self):
        DRIVER.get("https://dev-layout-cms.fox29.com/category")
        Page.select_layout("Entertainment")
        assert (
            DRIVER.current_url
            == "https://dev-layout-cms.fox29.com/category#entertainment"
        )
