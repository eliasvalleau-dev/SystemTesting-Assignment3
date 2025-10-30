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
        # Check if Adding Process Works
        if self.check_compare_product() == False:
            print("Failed to Remove Products from Comparison (Adding Process Failed)")
            return False
        
        # Click Remove Button
        try:
            remove_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div/table/tbody[2]/tr/td[2]/a")
            remove_btn.click()

            # Check if Removal Alert Is Correct
            if self.check_alert() == False:
                print("Failed to Remove Products from Comparison (Removal Alert Was Missing/Incorrect).")
                return False

            # Check if Rows Have Been Reduced
            elif len(self.driver.find_elements(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div/table/tbody[1]/tr[1]")) == 1:
                print("Successfully Removed Product from Comparison.")
                return True
            
            # Exception Case if Number of Columns Aren't Reduced
            else:
                print("Failed to Remove Products from Comparison (Number of Columns Doesn't Match Expected).")
                return False

        # Exception for if Selenium Can’t Find a Given Element
        except NoSuchElementException:
            print("Failed to Remove Products from Comparison (Webdriver Couldn't Find Requested Element).")
        
        # Exception for Generic Errors
        except Exception as e:
            print(f"Failed to Remove Products from Comparison (Unknown Exception: {e})")
        
        return False

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

    def add_comparison(self, obj) -> bool:
        '''Instance Method for Clicking the Product's Compare Button'''
        # Click Product and Then Click Compare Button
        try:
            obj.click()
            compare_btm = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[9]/div[1]/div[2]/div/div[2]/div[2]/div[10]/div/div[5]/button")
            compare_btm.click()
            self.driver.back()
            return True
        
        # Exception for if Selenium Can’t Find a Given Element
        except NoSuchElementException:
            print("Failed to Add Product to Comparison (Webdriver Couldn't Find Compare Button)")
        
        # Exception for Generic Errors
        except Exception as e:
            print(f"Failed to Add Product to Comparison (Unknown Exception: {e}).")
        
        return False

    def check_alert(self) -> bool:
        '''Instance Method for Checking if Alert is Present (Causes Changes To Relevant XPATH)'''
        # Get Alert Message
        try:
            alert = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div[1]").text

            # Close Alert
            alert_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div[1]")
            alert_button.click()


            # Determine if Alert Was Successful
            if alert == "Success: You have modified your product comparison!\n×":
                return True
            return False
        
        # Exception for if Selenium Can’t Find a Given Element
        except NoSuchElementException:
            print("Failed to Remove Products From Comparison (Webdriver Couldn't Find Alert).")
        
        # Exception for Generic Errors
        except Exception as e:
            print(f"Failed to Removing Products From Comparison (Unknown Exception: {e}).")
        
        return False

    def modify_entry(obj, text) -> None:
        '''Static Method for Overriding Entry Elements'''
        obj.clear()
        obj.send_keys(text)
    
    def close(self) -> None:
        self.driver.quit()

if __name__ == "__main__":
    #login = Test(url='https://ecommerce-playground.lambdatest.io/index.php?route=account/login')
    # print(login.check_submit_review())
    # print(login.check_blog_comment())
    # print(login.check_quantity())
    #login.close()
    
    # Test for Comparing Products
    #comp_test = Test(url="https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=20")
    #comp_test.check_compare_product()
    #comp_test.close()

    # Test for Removing Product Comparisons
    #rem_comp_test = Test(url="https://ecommerce-playground.lambdatest.io/index.php?route=product/category&path=20")
    #rem_comp_test.check_remove_comparison()
    #rem_comp_test.close()

    # Test for Modifying Affiliate Information
    #aff_test = Test(url="https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
    #aff_test.check_modify_affiliate()
    #aff_test.close()
    pass
