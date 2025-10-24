from selenium import webdriver
import time
from selenium.webdriver.common.by import By

class Test():
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
    
    def check_login(self):
        email_entry = self.driver.find_element(By.ID, "input-email")
        email_entry.send_keys("elias.valle@student.uts.edu.au")
        pass_entry = self.driver.find_element(By.ID, "input-password")
        pass_entry.send_keys("Loginpage@")
    
    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    login_test = Test(url="https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
    login_test.check_login()
    login_test.close()