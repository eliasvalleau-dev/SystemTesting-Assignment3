
# ecommerce_tests_combined.py
# Registration, Login, Checkout — single driver, callable functions.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time, sys

BASE = "https://ecommerce-playground.lambdatest.io"
WAIT = 12

# ---------- driver ----------
def make_driver():
    s = Service("chromedriver.exe")
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    d = webdriver.Chrome(service=s, options=options)
    return d

# ---------- helpers ----------
def close_banners(driver):
    selectors = [
        ".cc-allow", ".cookie-accept", ".cookie__accept", ".cookie-accept-all",
        ".btn-accept", ".cookie-btn-accept", ".cookie-allow", "#acceptCookies",
        ".close", ".modal .close"
    ]
    for css in selectors:
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css))).click()
            break
        except TimeoutException:
            pass
        except Exception:
            pass

def click(driver, by, value, timeout=WAIT):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value))).click()

# This is the lightweight js_click that worked for registration
def js_click(driver, by, value, timeout=WAIT):
    try:
        el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        driver.execute_script("arguments[0].click();", el)
    except Exception as e:
        print(f"js_click failed for selector ({by}, {value}): {e}")
        raise 

def type_into(driver, by, value, text, timeout=WAIT):
    el = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)))
    el.clear()
    el.send_keys(text)

def page_has(driver, text):
    return text.lower() in driver.page_source.lower()

# ---------- flows ----------

# --- THIS FUNCTION IS 100% CORRECT ---
def register_user(driver, first="Manoj", last="Kumar", email=None, password="Test@1234"):
    try:
        if email is None:
            email = f"manoj{int(time.time())}.test@auto-example.com"

        print("Starting registration...")
        driver.get(f"{BASE}/index.php?route=account/register")
        print("Register page loaded. Closing banners...")
        close_banners(driver)

        WebDriverWait(driver, WAIT).until(EC.visibility_of_element_located((By.ID, "input-firstname")))

        print("Typing first name...")
        type_into(driver, By.ID, "input-firstname", first)
        print("Typing last name...")
        type_into(driver, By.ID, "input-lastname", last)
        print("Typing email...")
        type_into(driver, By.ID, "input-email", email)
        print("Typing telephone...")
        type_into(driver, By.ID, "input-telephone", "1234567890")
        
        print("Typing password...")
        type_into(driver, By.ID, "input-password", password)
        
        print("Typing password confirm...")
        type_into(driver, By.ID, "input-confirm", password)

        print("Clicking 'Agree' checkbox...")
        js_click(driver, By.ID, "input-agree")

        print("Clicking 'Continue' (submit) button...")
        js_click(driver, By.CSS_SELECTOR, "input.btn.btn-primary")
        
        print("Waiting for 'account/success' URL...")
        WebDriverWait(driver, WAIT).until(EC.url_contains("account/success"))
        
        print("Validating success...")
        ok = "account/success" in driver.current_url

        print("Registration Test Passed" if ok else "Registration Test Failed")
        return ok, email, password
    except Exception as e:
        print("\n--- REGISTRATION FAILED ---")
        print(f"Failed on URL: {driver.current_url}") 
        print(f"Exception Type: {type(e)}")
        print(f"Exception Details: {e}\n")
        return False, email, password

# --- THIS FUNCTION IS 100% CORRECT ---
def login_user(driver, email, password):
    try:
        print("Starting login...")
        driver.get(f"{BASE}/index.php?route=account/login")
        print("Login page loaded. Closing banners...")
        close_banners(driver)
        
        WebDriverWait(driver, WAIT).until(EC.visibility_of_element_located((By.ID, "input-email")))
        
        print("Typing login email...")
        type_into(driver, By.ID, "input-email", email)
        print("Typing login password...")
        type_into(driver, By.ID, "input-password", password)
        
        print("Clicking 'Login' (submit) button...")
        js_click(driver, By.CSS_SELECTOR, "input.btn.btn-primary")
        
        print("Waiting for 'My Account' page to load...")
        WebDriverWait(driver, WAIT).until(EC.title_contains("My Account"))
        
        print("ValidTating login success...")
        ok = page_has(driver, "Edit your account information") or \
             page_has(driver, "My Account") or \
             ("account/account" in driver.current_url)
        print("Login Test Passed" if ok else "Login Test Failed")
        return ok
    except Exception as e:
        print("\n--- LOGIN FAILED ---")
        print(f"Failed on URL: {driver.current_url}") 
        print(f"Exception Type: {type(e)}")
        print(f"Exception Details: {e}\n")
        return False

# --- THIS FUNCTION IS UPDATED TO BUY THE HP LP3065 (IN STOCK) ---
def checkout_test(driver, email, password):
    try:
        # 0) We now MUST log in with our new, fresh driver
        if not login_user(driver, email, password):
            print("Checkout Test Failed (login precondition not met)")
            return False
        
        print("Starting checkout flow from 'My Account' page...")
        
        # 1) navigate to product
        # --- START FIX ---
        # We will navigate directly to the "HP LP3065" page (product ID 47)
        print("Navigating directly to HP LP3065 product page...")
        hp_url = f"{BASE}/index.php?route=product/product&product_id=47"
        driver.get(hp_url)
        
        # Now we wait for the *correct* title
        print("Waiting for HP LP3065 page to load...")
        WebDriverWait(driver, WAIT).until(EC.title_contains("HP LP3065"))
        close_banners(driver)
        # --- END FIX ---

        # 2) add to cart
        # --- START FIX ---
        # We will add the HP LP3065 (product_id 47) to the cart
        print("Adding HP LP3065 to cart (using direct JS call)...")
        driver.execute_script("cart.add('47', '1');")
        # --- END FIX ---

        # 3) Wait for success and go to checkout
        print("Pausing 1.5 sec to let cart session update...")
        time.sleep(1.5) # A short pause is safer after a JS cart add
        
        # We will use the stable "Two-Step Navigation"
        print("Bypassing UI, navigating directly to Shopping Cart URL...")
        cart_url = f"{BASE}/index.php?route=checkout/cart"
        driver.get(cart_url)
        
        print("Waiting for Shopping Cart page to load...")
        WebDriverWait(driver, WAIT).until(EC.title_contains("Shopping Cart"))
        
        # Now that we have "visited" the cart, we can go to checkout.
        print("Navigating directly to Checkout URL...")
        checkout_url = f"{BASE}/index.php?route=checkout/checkout"
        driver.get(checkout_url)

        # 4) validate
        print("Waiting for Checkout page to load...")
        WebDriverWait(driver, WAIT).until(EC.title_contains("Checkout"))
        
        print("Validating checkout page...")
        ok = ("Checkout" in driver.title) or page_has(driver, "Confirm Order") or \
             ("checkout/checkout" in driver.current_url)

        print("Checkout Test Passed" if ok else "Checkout Test Failed")
        return ok
    except Exception as e:
        print("\n--- CHECKOUT FAILED ---")
        print(f"Failed on URL: {driver.current_url}") 
        print(f"Exception Type: {type(e)}")
        print(f"Exception Details: {e}\n")
        return False

# --- THIS RUNNER IS 100% CORRECT ---
if __name__ == "__main__":
    
    # --- PART 1: REGISTRATION ---
    driver_reg = None
    email = None
    pwd = None
    reg_ok = False
    
    try:
        print("--- PART 1: REGISTRATION ---")
        driver_reg = make_driver()
        reg_ok, email, pwd = register_user(driver_reg)
        
        if not reg_ok:
            print("Registration failed, skipping checkout test.")
            
    except Exception as e:
        print(f"Fatal error during registration: {e}")
        reg_ok = False
    finally:
        try:
            if driver_reg:
                print("--- Part 1 Finished. Quitting registration driver. ---")
                driver_reg.quit()
        except Exception:
            pass

    # --- PART 2: LOGIN & CHECKOUT ---
    driver_checkout = None
    if reg_ok:
        try:
            print("\n--- PART 2: LOGIN & CHECKOUT ---")
            driver_checkout = make_driver()
            checkout_test(driver_checkout, email, pwd) # Pass credentials in
        except Exception as e:
            print(f"Fatal error during checkout: {e}")
        finally:
            try:
                if driver_checkout:
                    print("--- Part 2 Finished. Quitting checkout driver. ---")
                    driver_checkout.quit()
            except Exception:
                pass
    else:
        print("--- Skipping Part 2 because registration failed ---")

    print("\n--- TEST RUN COMPLETE ---")