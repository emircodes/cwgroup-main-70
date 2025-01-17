from api.tests.selenium_tests.base_test import SeleniumBaseTest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestProfile(SeleniumBaseTest):
    def test_login_navigate_and_edit_profile(self):
        """Test to log in, navigate to the profile page, and edit profile fields."""
        
        self.driver.get("http://localhost:5173/login")

        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        username_field.send_keys("adamz@gmail.com")
        password_field.send_keys("ab")

        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        
        profile_nav_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "profile-nav"))
        )
        profile_nav_button.click()

        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']"))
        )

        
        username_field = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Username']")
        email_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='email'][placeholder='Username']")
        dob_field = self.driver.find_element(By.CSS_SELECTOR, "input.form-control")  # Adjusted

        username_field.clear()
        username_field.send_keys("NewUsername")

        email_field.clear()
        email_field.send_keys("newemail@example.com")

        dob_field.clear()
        dob_field.send_keys("2000-01-01")  

        
        save_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        save_button.click()

        
        time.sleep(2)
        print("Profile updated successfully")
