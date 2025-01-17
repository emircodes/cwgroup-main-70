from api.tests.selenium_tests.base_test import SeleniumBaseTest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestLogin(SeleniumBaseTest):
    def test_valid_login(self):
        
        self.driver.get("http://localhost:5173/login")

        
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        username_field.send_keys("adamz@gmail.com")
        password_field.send_keys("ab")

        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        
        time.sleep(2)
        print("Current URL:", self.driver.current_url)
        print(self.driver.page_source)

