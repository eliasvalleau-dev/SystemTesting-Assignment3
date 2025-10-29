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
        # User Login
        email_entry = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "input-email"))
        )
        email_entry.send_keys("elias.valle@student.uts.edu.au")

        pass_entry = self.driver.find_element(By.ID, "input-password")
        pass_entry.send_keys("Loginpage@" + Keys.ENTER) 
        time.sleep(5)

        # Validation
        if self.driver.current_url == "https://ecommerce-playground.lambdatest.io/index.php?route=account/account":
            return True
        return False
    
    def check_submit_review(self) -> bool:    
        if self.check_login() == False:
            print("Failed to login")
            return False
        print("Succesfully Logged into Account")

        try:
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
            print("Successfully selected HTC Touch HD")

            # Insert review and submit
            input_rating = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='rating-3-216860']"))
            )
            input_rating.click()
            input_description = self.driver.find_element(By.ID, "input-review")
            input_description.send_keys("I think this product is exceptionally well manufactured, great job!!")
            submit_button = self.driver.find_element(By.ID, "button-review").click()
            print("Successfully rated product and wrote review")

            # Validation
            success_alert = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success.alert-dismissible"))
            )
            if(success_alert.is_displayed()):
                self.driver.save_screenshot("submitReview.png")
                print("Successfully commented about the product, HTC Touch HD")
                return True
        
        # Exception Handling 
        except NoSuchElementException:
            print("Program Terminated. Webdriver Could Not Find Requested Element")

        except Exception as e:
            print(f"Webdriver Terminated Program Due To An Unknown Exception: {e}")

        return False
    
    def check_blog_comment(self) -> bool:
        if self.check_login() == False:
            print("Failed to login")
            return False
        print("Successfully Logged into Account")
        
        try:
            # Navigate to Blog Page
            blog_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/header/div[3]/div[1]/div/div[3]/nav/div/ul/li[3]/a"))
            )
            blog_element.click()

            # Choose blog
            time.sleep(5)
            blog_choice = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(((By.XPATH, "/html/body/div[1]/div[5]/div[1]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div[1]/a")))
            )
            blog_choice.click()
            print("Successfully Navigated to a Blog Page")

            # Write comment & post
            comment_input = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "input-comment"))
            )
            comment_input.clear()
            comment_input.send_keys("This is a great blog post! Very informative and well written!!!")
            post_comment = self.driver.find_element(By.ID, "button-comment").click()
            print("Writing comment on blog")
            time.sleep(5)

            # Validation
            success_alert = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-success.alert-dismissible"))
            )
            if(success_alert.is_displayed()):
                # self.driver.save_screenshot("blogComment.png")
                print("Successfully commented on blog")
                return True
            
        # Exception Handling 
        except NoSuchElementException:
            print("Program Terminated. Webdriver Could Not Find Requested Element")

        except Exception as e:
            print(f"Webdriver Terminated Due To An Unknown Exception{e}")

        return False
    
    def check_quantity(self) -> bool:
        try:
            # Search for product
            search_bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search"))
            )
            search_bar.send_keys("HTC Touch HD" + Keys.ENTER)

            # Select Product
            product_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "mz-product-grid-image-53-212469"))
            )
            product_element.click()
            print("Successfully selected HTC Touch HD")

            # Enter quantity & add to Cart
            input_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div[10]/div/div[4]/div/div[1]/div/div[2]/button"))
            )
            for i in range(5):
                input_button.click()
                time.sleep(1)
                print(f"Quantity: {i+2}")
            checkout_button = self.driver.find_element(By.CSS_SELECTOR, "button[title='Buy now']").click()
            print()

            # Validation
            product_amount = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div/form/div/div[2]/div/div[1]/div[1]/table/tbody/tr/td[3]/div/input"))
            )
            amount = product_amount.get_attribute("value")
            # self.driver.save_screenshot("productQuantity.png")
            remove_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div/form/div/div[2]/div/div[1]/div[1]/table/tbody/tr/td[3]/div/div/button[2]")
            remove_button.click()
            
            return amount == "6"

        # Exception Handling 
        except NoSuchElementException:
            print("Program Terminated. Webdriver Could Not Find Requested Element")

        except Exception as e:
            print(f"Webdriver Terminated Program Due To An Unknown Exception: {e}")
        
        return False

    
    def close(self) -> None:
        self.driver.quit()

if __name__ == "__main__":
    login_test = Test(url='https://ecommerce-playground.lambdatest.io/index.php?route=account/account')
    # print(login_test.check_submit_review())
    # print(login_test.check_blog_comment())
    print(login_test.check_quantity())
    login_test.close()
    