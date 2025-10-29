from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Test():
    def __init__(self, url) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get(url)
    
    def check_login(self) -> bool:
        email_entry = self.driver.find_element(By.ID, "input-email")
        email_entry.send_keys("elias.valle@student.uts.edu.au")
        pass_entry = self.driver.find_element(By.ID, "input-password")
        pass_entry.send_keys("Loginpage@")
        submit_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div/div/div[2]/div/div/form/input")
        submit_btn.click()

        if self.driver.current_url == "https://ecommerce-playground.lambdatest.io/index.php?route=account/account":
            print("Login Successful")
            return True
        print("Login Unsuccessful")
        return False
    
    def check_compare_product(self) -> bool:
        pass

    def check_remove_comparison(self) -> bool:
        pass

    def check_modify_affiliate(self) -> bool:
        if self.check_login() == False:
            print("Failed to Modify Affiliate Information (Login Failed).")
            return False
        try:
            edit_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div/div[3]/div/a[1]")
            edit_btn.click()
            comp_entry = self.driver.find_element(By.ID, "input-company")
            comp_entry.clear()
            Test.modify_entry(comp_entry, "Test Inc")
            web_entry = self.driver.find_element(By.ID, "input-website")
            Test.modify_entry(web_entry, "https://www.example.com/")
            tax_entry = self.driver.find_element(By.ID, "input-tax")
            Test.modify_entry(tax_entry, "444444444")
            cheque_option = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div/form/fieldset[2]/div[2]/div/div[1]/label/input")
            cheque_option.click()
            cheque_name = self.driver.find_element(By.ID, "input-cheque")
            Test.modify_entry(cheque_name, "John Smith")
            confirm_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div/form/div/div/input")
            confirm_btn.click()
            alert = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div[1]").text
            if alert == "Success: Your account has been successfully updated.":
                print("Successfully Modified Affiliate Information.")
                return True
            print("Failed to Modify Affiliate Information (Incorrect Alert).")
        except NoSuchElementException:
            print("Failed to Modify Affiliate Information (Webdriver Couldn't Find Request Element).")
        except Exception as e:
            print(f"Failed to Modify Affiliate Information (Unknown Exception: {e})")
        return False
    
    # Piggybacks onto check_login()
    def submit_review(self) -> bool:    

        # Search for product
        search_bar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "search"))
        )
        search_bar.send_keys("HTC Touch HD" + Keys.ENTER)

        # Select Product
        product_element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "mz-product-grid-image-28-212469"))
        )
        product_element.click()

        # Insert review and submit
        input_rating = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='rating-3-216860']"))
        )
        input_rating.click()
        input_description = self.driver.find_element(By.ID, "input-review")
        input_description.send_keys("I think this product is exceptionally well manufactured, great job!!")
        submit_button = self.driver.find_element(By.ID, "button-review").click()

        # Validation
        success_alert = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success.alert-dismissible"))
        )
        if(success_alert.is_displayed()):
            return True
        return False
    
    def comment_blog(self) -> bool:
        return False
    
    def check_quantity(self) -> bool:
        return False

    def modify_entry(obj, text) -> None:
        obj.clear()
        obj.send_keys(text)
    
    def close(self) -> None:
        self.driver.quit()

if __name__ == "__main__":
    # Test for Comparing Products
    #comp_test = Test(url="https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=20")

    # Test for Removing Product Comparisons
    #rem_comp_test = Test(url="https://ecommerce-playground.lambdatest.io/index.php?route=product/compare")

    # Test for Modifying Affiliate Information
    aff_test = Test(url="https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
    aff_test.check_modify_affiliate()
    aff_test.close()
    
