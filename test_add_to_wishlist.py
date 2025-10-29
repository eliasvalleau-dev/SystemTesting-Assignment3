from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def test_add_to_wishlist():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)
    actions = ActionChains(driver)
    try:
        # Step 1: Navigate to homepage
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=common/home")

        # Step 2: Go to login page
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")

        # Step 3: Log in
        wait.until(EC.presence_of_element_located((By.ID, "input-email"))).send_keys("testuser@example.com.au")
        driver.find_element(By.ID, "input-password").send_keys("oldpassword123")
        driver.find_element(By.CSS_SELECTOR, "input.btn-primary").click()
        wait.until(EC.presence_of_element_located((By.ID, "content")))

        # Step 4: Go to home page
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=common/home")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-thumb")))

        # Step 5: Locate the product (iMac)
        product = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='iMac']"))
        )

        # Step 6: Hover and click wishlist icon
        actions.move_to_element(product).perform()
        time.sleep(1)
        wishlist_icon = product.find_element(By.XPATH, "../../..//i[contains(@class, 'fa-heart')]")
        driver.execute_script("arguments[0].click();", wishlist_icon)

        # Step 7: Wait for success notification
        try:
            success_box = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@id='notification-box-top']//div[contains(., 'Success: You have added')]"))
            )
            print("Success notification detected.")
        except TimeoutException:
            print("Success notification not detected, continuing safely.")

        # Step 8: Navigate directly to wishlist page
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/wishlist")

        # Step 9: Confirm wishlist contains the product
        wishlist_items = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.table tbody tr"))
        )
        found = any("iMac" in item.text for item in wishlist_items)
        assert found, "iMac not found in wishlist."
        print("iMac successfully added to wishlist.")

        # Step 10: Remove the item from wishlist
        remove_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[i[@class='fa fa-times']]"))
        )
        driver.execute_script("arguments[0].click();", remove_button)

        # Step 11: Confirm success alert after removal
        success_alert = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'alert-success') and contains(., 'Success: You have modified your wish list!')]"))
        )
        print("Wishlist removal confirmed via success message.")

        print("Test Case T005 Passed Successfully!")

    except Exception as e:
        print(f"Test Case T005 failed: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_add_to_wishlist()
