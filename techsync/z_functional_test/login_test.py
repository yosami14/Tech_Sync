from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class LoginTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/login/")

    def tearDown(self):
        self.driver.quit()

    def test_successful_login(self):
        driver = self.driver

        # Add a delay to ensure the server is up
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

        # Locate email and password fields and login button
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, '//input[@type="submit"]')

        # Input valid credentials
        email_field.send_keys("yosami14@gmail.com")
        password_field.send_keys("123")
        login_button.click()

        # Wait for the redirect to the home page and verify successful login
        WebDriverWait(driver, 10).until(EC.url_changes("http://127.0.0.1:8000/login/"))
        self.assertTrue(driver.current_url == "http://127.0.0.1:8000/")

    def test_unsuccessful_login(self):
        driver = self.driver

        # Locate email and password fields and login button
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, '//input[@type="submit"]')

        # Input invalid credentials
        email_field.send_keys("wrongemail@example.com")
        password_field.send_keys("wrongpassword")
        login_button.click()

        # Wait for the error message and verify it is displayed
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert")))
            error_message = driver.find_element(By.CSS_SELECTOR, ".alert").text
            self.assertIn("Invalid email or password.", error_message)
        except Exception as e:
            print("Error message element not found or other issue:")
            raise e

if __name__ == "__main__":
    unittest.main()
