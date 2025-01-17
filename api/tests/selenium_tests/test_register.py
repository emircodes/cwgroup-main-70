from api.tests.selenium_tests.base_test import SeleniumBaseTest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestRegister(SeleniumBaseTest):
    def test_valid_registration(self):
        
        self.driver.get("http://localhost:5173/register")

        
        name_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Name']"))
        )
        email_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Email']")
        password_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")

        
        name_field.send_keys("Test User")
        email_field.send_keys("testuser@example.com")
        password_field.send_keys("securepassword")

        
        register_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        register_button.click()

        
        time.sleep(2)

        
        current_url = self.driver.current_url
        

        
        print("Current URL:", current_url)
        print(self.driver.page_source)
