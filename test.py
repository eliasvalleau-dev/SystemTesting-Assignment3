from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

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
        # Get Products Being Tested
        product1 = self.driver.find_element(By.ID, "mz-product-grid-image-28-212408")
        product2 = self.driver.find_element(By.ID, "mz-product-grid-image-29-212408")

        # Test if Products Can Be Added to Comparison
        if self.add_comparison(product1) and self.add_comparison(product2):
            
            # Open Comparison Page
            try:
                compare_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/header/div[2]/div[1]/div[3]/a")
                compare_btn.click()

                # Get Comparison Links
                comparison1 = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div/table/tbody[1]/tr[1]/td[2]/a")
                comparison2 = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div/table/tbody[1]/tr[1]/td[3]/a")

                # Check Comparison Text
                if comparison1.text == "HTC Touch HD" and comparison2.text == "Palm Treo Pro":
                    print("Successfully Compared Two Products.")
                    return True
            
            # Exception for if Selenium Can’t Find a Given Element
            except NoSuchElementException:
                print("Failed to Compare Products (Webdriver Couldn't Find Requested Element).")
            
            # Exception for Generic Errors
            except Exception as e:
                print(f"Failed to Compare Products (Unknown Exception: {e}).")

        return False


    def check_remove_comparison(self) -> bool:
        pass

    def check_modify_affiliate(self) -> bool:
        # Check if User Has Logged In
        if self.check_login() == False:
            print("Failed to Modify Affiliate Information (Login Failed).")
            return False
        
        # Open 'Edit Affiliate Information' Page
        try:    
            edit_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div/div[3]/div/a[1]")
            edit_btn.click()
            
            # Enter Affiliate Details
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
            
            # Confirm Affiliate Details
            confirm_btn.click()
            
            # Check if Success Alert on Account Page Is Present
            alert = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div[1]").text
            if alert == "Success: Your account has been successfully updated.":
                print("Successfully Modified Affiliate Information.")
                return True
            print("Failed to Modify Affiliate Information (Incorrect Alert).")
        
        # Exception for if Selenium Can’t Find a Given Element
        except NoSuchElementException:
            print("Failed to Modify Affiliate Information (Webdriver Couldn't Find Requested Element).")
        
        # Exception for Generic Errors
        except Exception as e:
            print(f"Failed to Modify Affiliate Information (Unknown Exception: {e})")
        
        return False
    
    def submit_review(self) -> bool:
        return False
    
    def comment_blog(self) -> bool:
        return False
    
    def check_quantity(self) -> bool:
        return False

    def add_comparison(self, obj) -> bool:
        # Click Product and Then Click Compare Button
        try:
            obj.click()
            compare_btm = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div[10]/div/div[5]/button")
            compare_btm.click()
            self.driver.back()
            return True
        
        # Exception for if Selenium Can’t Find a Given Element
        except NoSuchElementException:
            print("Adding Product to Comparison Failed (Webdriver Couldn't Find Compare Button)")
        
        # Exception for Generic Errors
        except Exception as e:
            print(f"Adding Product to Comparison Failed (Unknown Exception: {e}).")
        
        return False

    def modify_entry(obj, text) -> None:
        '''Static Method for Overriding Entry Elements'''
        obj.clear()
        obj.send_keys(text)
    
    def close(self) -> None:
        self.driver.quit()

if __name__ == "__main__":
    # Test for Comparing Products
    comp_test = Test(url="https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=20")
    comp_test.check_compare_product()
    comp_test.close()

    # Test for Removing Product Comparisons
    #rem_comp_test = Test(url="https://ecommerce-playground.lambdatest.io/index.php?route=product/compare")

    # Test for Modifying Affiliate Information
    #aff_test = Test(url="https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
    #aff_test.check_modify_affiliate()
    #aff_test.close()
    pass