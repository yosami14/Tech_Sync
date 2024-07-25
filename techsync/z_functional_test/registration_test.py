from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/register/")

    def tearDown(self):
        self.driver.quit()

    def test_successful_registration(self):
        driver = self.driver

        # Add a delay to ensure the server is up
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        # Locate form fields
        first_name_field = driver.find_element(By.NAME, "first_name")
        username_field = driver.find_element(By.NAME, "username")
        email_field = driver.find_element(By.NAME, "email")
        password1_field = driver.find_element(By.NAME, "password1")
        password2_field = driver.find_element(By.NAME, "password2")
        submit_button = driver.find_element(By.XPATH, '//input[@type="submit"]')

        # Input valid registration details
        first_name_field.send_keys("John Doe")
        username_field.send_keys("johndoe")
        email_field.send_keys("johndoe@example.com")
        password1_field.send_keys("strongpassword")
        password2_field.send_keys("strongpassword")
        submit_button.click()

        # Wait for the redirect to the edit account page and verify successful registration
        WebDriverWait(driver, 10).until(EC.url_contains("http://127.0.0.1:8000/edit-account/"))
        self.assertTrue(driver.current_url.endswith("/edit-account/"))


        # Verify the success message
        success_message = driver.find_element(By.CSS_SELECTOR, ".alert--info").text
        self.assertIn("Please complete your profile", success_message)

    def test_unsuccessful_registration(self):
        driver = self.driver

        # Locate form fields
        first_name_field = driver.find_element(By.NAME, "first_name")
        username_field = driver.find_element(By.NAME, "username")
        email_field = driver.find_element(By.NAME, "email")
        password1_field = driver.find_element(By.NAME, "password1")
        password2_field = driver.find_element(By.NAME, "password2")
        submit_button = driver.find_element(By.XPATH, '//input[@type="submit"]')

        # Input invalid registration details (passwords do not match)
        first_name_field.send_keys("John Doe2")
        username_field.send_keys("johndoe2")
        email_field.send_keys("johndoe2@example.com")
        password1_field.send_keys("strongpassword")
        password2_field.send_keys("differentpassword")
        submit_button.click()

        # Wait for the error message and verify it is displayed
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".form__field .error")))
            error_message = driver.find_element(By.CSS_SELECTOR, ".form__field .error").text
            self.assertIn("The two password fields didn’t match.", error_message)
        except Exception as e:
            print("Error message element not found or other issue:")
            raise e

if __name__ == "__main__":
    unittest.main()
