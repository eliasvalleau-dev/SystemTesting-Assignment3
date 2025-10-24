from selenium import webdriver
import time
from selenium.webdriver.common.by import By

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
            return True
        return False
    
    def close(self) -> None:
        self.driver.quit()

if __name__ == "__main__":
    login_test = Test(url="https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
    print(login_test.check_login())
    login_test.close()