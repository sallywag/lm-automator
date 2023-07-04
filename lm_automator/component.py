from lm_automator.widget import Widget
from lm_automator.inputs import Button
from lm_automator.element_handler import wait_after_for_timeout


class Component(Widget):

    def __init__(
        self,
        locator: str,
        position: int
    ):
        super().__init__(locator)
        self.position = position
        self._edit = Button(self.locator + " .fa-pencil")
        self._delete = Button(self.locator + " .fa-times")
        self._confirm = Button(".swal2-confirm.swal2-styled")

    @wait_after_for_timeout(reason="Ensure menu is fully expanded.")
    def edit(self) -> None:
        """Edit the component.

		User Flow:
		1. Click the edit button of the component you wish to edit.
		"""
        self._edit.click()

    def delete(self) -> None:
        """Delete the component.

		User Flow:
		1. Click the delete button of the component you wish to delete.
		"""
        self._delete.click()
        self._confirm.click()

    @property
    def locator(self) -> str:
        return f"{self._locator}:nth-child({self.position})"
