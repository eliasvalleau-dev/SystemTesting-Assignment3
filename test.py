from selenium import webdriver
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome() #start a session

# navigate to a web page
driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=common/home")

title = driver.title # request browser information
print(title)

driver.implicitly_wait(0.5) # wait for 0.5 seconds
text_box = driver.find_element(by=By.NAME, value="search") # find a specific text box
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button") # find the only button on the page

text_box.send_keys("hello")



time.sleep(10)
driver.quit() #end a session


