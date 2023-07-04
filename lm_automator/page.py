from lm_automator.element_handler import ElementHandler
from lm_automator.inputs import Button, Text


class Page:

    caret_button = Button(".category-selector .btn.btn-info.dropdown-toggle")
    filter_button = Text(".category-selector input.dropdown-filter")
    publish_button = Button(".content-header .btn-submit")
    confirm_button = Button(".swal2-container .swal2-confirm")

    @classmethod
    def select_layout(cls, layout: str) -> None:
        """Go to the specified layout.

		User Flow:
		1. Click the caret button.
		2. Enter the layout name into the search bar.
		3. Click the layouts name.
		"""
        cls.caret_button.click()
        cls.filter_button.value = layout
        ElementHandler.click_element(
            ".category-selector .dropdown-menu li:nth-child(3)"
        )
        ElementHandler.wait_for_timeout(reason="Ensure page is fully loaded.")

    @classmethod
    def visit(cls, name: str) -> None:
        """Visit the URL specified by the name parameter.

        User Flow:
        1. Click the sidebar item of the page you wish to visit.
        """
        ElementHandler.click_element(f'.main-sidebar [href="/{name}"]')
        ElementHandler.wait_for_timeout(reason="Ensure page is fully loaded.")

    @classmethod
    def publish(cls) -> None:
        """Publish the page and wait to ensure the API is updated
        before continuing.

        User Flow:
        1. Click the publish button.
        2. Click the confirm button in the pop up.
        """
        cls.publish_button.click()
        cls.confirm_button.click()
        ElementHandler.wait_for_timeout(reason="Ensure published changes reflect in the API.")
