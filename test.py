from selenium import webdriver
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
        # User Login
        email_entry = self.driver.find_element(By.ID, "input-email")
        email_entry.send_keys("elias.valle@student.uts.edu.au")
        pass_entry = self.driver.find_element(By.ID, "input-password")
        pass_entry.send_keys("Loginpage@") # pass_entry.send_keys("Loginpage@" + Keys.ENTER) may increase readability
        submit_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div/div/div[2]/div/div/form/input")
        submit_btn.click()
        # Validation
        if self.driver.current_url == "https://ecommerce-playground.lambdatest.io/index.php?route=account/account":
            return True
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

    
    def close(self) -> None:
        self.driver.quit()

if __name__ == "__main__":
    login_test = Test(url="https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
    print(login_test.check_login())
    print(login_test.submit_review())
    login_test.close()
    