from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_change_password():
    """T006 – Test updating a user's password using direct URL navigation"""
    driver = webdriver.Chrome()
    driver.maximize_window()

    old_password = "oldpassword123"
    new_password = "newpassword123"
    email = "testuser@example.com.au"

    try:
        # Step 1: Navigate directly to login page
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")

        # Step 2: Enter login credentials
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-email"))
        )
        password_input = driver.find_element(By.ID, "input-password")
        email_input.clear()
        password_input.clear()
        email_input.send_keys(email)
        password_input.send_keys(old_password)

        # Submit login form
        login_button = driver.find_element(By.XPATH, "//input[@value='Login']")
        login_button.click()

        # Step 3: Navigate directly to password update page
        # Wait for dashboard to load
        dashboard_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(),'My Account')]"))
        )

        # Locate the sidebar Password link
        password_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[@href='https://ecommerce-playground.lambdatest.io/index.php?route=account/password']")
            )
        )
        password_link.click()

        # Step 4: Enter new password and confirm
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-password"))
        )
        confirm_field = driver.find_element(By.ID, "input-confirm")
        password_field.clear()
        password_field.send_keys(new_password)
        confirm_field.clear()
        confirm_field.send_keys(new_password)

        # Step 5: Click continue
        continue_button = driver.find_element(By.XPATH, "//input[@value='Continue']")
        continue_button.click()

        # Step 6: Verify success message
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "successfully updated" in success_message.text.lower(), "Password update failed."
        print("Password updated successfully.")

        # Step 7: Log out using direct logout URL
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/logout")
        print("Logged out successfully.")

        # Step 8: Log back in with new password
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-email"))
        )
        password_input = driver.find_element(By.ID, "input-password")
        email_input.clear()
        password_input.clear()
        email_input.send_keys(email)
        password_input.send_keys(new_password)

        login_button = driver.find_element(By.XPATH, "//input[@value='Login']")
        login_button.click()

        # Verify login successful
        dashboard_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(),'My Account')]"))
        )
        print("Successfully logged in with new password.")

        # Optional: revert password back to old password for test repeatability
        # Repeat Steps 3–5 with old_password

    except Exception as e:
        print(f"Test Case T006 failed: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_change_password()
