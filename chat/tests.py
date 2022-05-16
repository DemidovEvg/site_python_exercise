from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from channels.testing import ChannelsLiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service


print('111111111111 test')

# chrome_options = Options()
# chrome_options.add_argument('start-maximized')
# service = Service(executable_path=ChromeDriverManager().install())
# # breakpoint()
# driver = webdriver.Chrome(
#     service=service,
#     options=chrome_options)

# driver.get("http://www.python.org")


class ChatTests(ChannelsLiveServerTestCase):
    # serve_static = True  # emulate StaticLiveServerTestCase

    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     print('1111111111111setUpClass')
    #     try:
    #         pass
    #         # cls.driver = driver
    #     except Exception as e:
    #         # breakpoint()
    #         print(e)
    #         super().tearDownClass()
    #         raise

    # @classmethod
    # def tearDownClass(cls):
    #     # cls.driver.quit()
    #     super().tearDownClass()

    def test_test1(self):
        self.assertEqual(1*1, 2)

    # def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
    #     try:
    #         self._enter_chat_room('room_1')

    #         self._open_new_window()
    #         self._enter_chat_room('room_1')

    #         self._switch_to_window(0)
    #         self._post_message('hello')

    #         WebDriverWait(self.driver, 2).until(
    #             lambda _:
    #             'hello' in self._chat_log_value,
    #             'Message was not received by window 1 from window 1')
    #         self._switch_to_window(1)
    #         WebDriverWait(self.driver, 2).until(
    #             lambda _:
    #             'hello' in self._chat_log_value,
    #             'Message was not received by window 2 from window 1')
    #     finally:
    #         self._close_all_new_windows()

    # def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
        # try:
        #     self._enter_chat_room('room_1')

        #     self._open_new_window()
        #     self._enter_chat_room('room_2')

        #     self._switch_to_window(0)
        #     self._post_message('hello')
        #     WebDriverWait(self.driver, 2).until(lambda _:
        #                                         'hello' in self._chat_log_value,
        #                                         'Message was not received by window 1 from window 1')

        #     self._switch_to_window(1)
        #     self._post_message('world')
        #     WebDriverWait(self.driver, 2).until(lambda _:
        #                                         'world' in self._chat_log_value,
        #                                         'Message was not received by window 2 from window 2')
        #     self.assertTrue('hello' not in self._chat_log_value,
        #                     'Message was improperly received by window 2 from window 1')
        # finally:
        #     self._close_all_new_windows()

    # === Utility ===

    # def _enter_chat_room(self, room_name):
    #     self.driver.get(self.live_server_url + '/chat/')
    #     ActionChains(self.driver).send_keys(room_name + '\n').perform()
    #     WebDriverWait(self.driver, 2).until(
    #         lambda _:
    #         room_name in self.driver.current_url)

    # def _open_new_window(self):
    #     self.driver.execute_script('window.open("about:blank", "_blank");')
    #     self.driver.switch_to_window(self.driver.window_handles[-1])

    # def _close_all_new_windows(self):
    #     while len(self.driver.window_handles) > 1:
    #         self.driver.switch_to_window(self.driver.window_handles[-1])
    #         self.driver.execute_script('window.close();')
    #     if len(self.driver.window_handles) == 1:
    #         self.driver.switch_to_window(self.driver.window_handles[0])

    # def _switch_to_window(self, window_index):
    #     self.driver.switch_to_window(self.driver.window_handles[window_index])

    # def _post_message(self, message):
    #     ActionChains(self.driver).send_keys(message + '\n').perform()

    # @property
    # def _chat_log_value(self):
    #     return self.driver.find_element_by_css_selector('#chat-log').get_property('value')
