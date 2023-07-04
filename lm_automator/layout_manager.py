from lm_automator.element_handler import ElementHandler
from lm_automator.common import DRIVER

class LayoutManager:

    def __init__(self, environment: str, site: str):
        self.environment = environment
        self.base_url = f'https://{self.environment}-layout-cms.{site}.com'

    def login(self, username: str, password: str) -> None:
        DRIVER.get(self.base_url)
        ElementHandler.send_keys_to_element('#idp-discovery-username', username)
        ElementHandler.click_element('#idp-discovery-submit')
        ElementHandler.send_keys_to_element('#okta-signin-password', password)
        ElementHandler.click_element('#okta-signin-submit')
        ElementHandler.click_element('.auth-content .button.button-primary')
        input('Hit enter after approving push:')
        