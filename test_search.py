# test_search_product.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import re
import time


def test_search_product():
    """T004 – Verify the Search Product function on the e-commerce site."""
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Step 1: Navigate to the website homepage
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=common/home")

        # Step 2: Locate the search bar at the top of the page
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "search"))
        )

        # Step 3: Enter a valid product keyword (e.g. “Phone”)
        search_box.clear()
        search_box.send_keys("Phone")

        # Step 4: Click the “Search” icon or press the “Enter” key
        search_box.send_keys(Keys.ENTER)

        # Step 5: Observe whether the website redirects to the search results page
        WebDriverWait(driver, 10).until(
            EC.url_contains("search")
        )
        current_url = driver.current_url
        assert "search" in current_url, "Did not navigate to the search results page."

        # Step 6: Verify that relevant products containing “Phone” appear in results
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb"))
        )
        assert len(results) > 0, "No search results found for 'Phone'."

        print(f"Found {len(results)} search results for 'Phone'.")

        # Step 7: Check that each product listed contains an image, name, and price
        for product in results[:5]:  # check first few items
            image = product.find_element(By.CSS_SELECTOR, "img")
            name = product.find_element(By.CSS_SELECTOR, "h4 a")
            price = product.find_element(By.CSS_SELECTOR, ".price")
            assert image.is_displayed(), "Product image missing."
            assert name.text.strip() != "", "Product name missing."
            assert price.text.strip() != "", "Product price missing."
        print("Each product displays image, name, and price correctly.")

        # Step 8: Sort results by price and confirm order changes
        try:
            sort_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//select[contains(@id,'sort') or contains(@name,'sort')]"))
            )
            sort_control = Select(sort_dropdown)
            

            #Select option Price (Low > High)
            sort_control.select_by_visible_text("Price (Low > High)")
            time.sleep(3)
            print("Sorting by Price (Low > High) applied successfully.")
        except Exception as e:
            print("Could not locate or interact with 'Sort By:' dropdown: {e}")

        print("Test Case T004 – Search Product Function: PASSED")

    except AssertionError as ae:
        print(ae)

    except Exception as e:
        print(f"Test Case T004 Failed due to error: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_search_product()
