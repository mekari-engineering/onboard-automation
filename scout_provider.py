from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import platform
import os
import time

class ScoutProvider:
    LOGIN_URL="https://scoutapm.com/users/sign_in"
    INVITE_URL="https://scoutapm.com/memberships"

    def __init__(self, email):
        self.email = email

    def onboard(self):
        driver = self.setup_driver()
        print("\n- Start onboarding Scout")

        try:
            self.sign_in(driver)
            self.invite_user(driver)
            self.check_invitation(driver)
            print("- Finish onboarding Scout")
        except Exception as e:
            print("- Error " + str(e))
        finally:
            driver.close()

    def sign_in(self, driver):
        driver.get(self.LOGIN_URL)
        print("- Sign In Scout")
        
        username_input = driver.find_element_by_name("user[email]")
        username_input.send_keys(os.environ["SCOUT_USERNAME"].strip())
        print("- Filling username")

        password_input = driver.find_element_by_name("user[password]")
        password_input.send_keys(os.environ["SCOUT_PASSWORD"].strip())
        print("- Filling password")

        driver.find_element_by_xpath("//input[@type='submit']").click()
        print("- Submit login form")
    
    def invite_user(self, driver):
        self.delay(2)

        driver.get(self.INVITE_URL)
        print("- Visit invite page")

        self.delay(2)
        
        email_input = driver.find_element_by_name("invite[email]")
        email_input.send_keys(self.email)
        print("- Invite email " + self.email)

        driver.find_element_by_xpath('//button[text()="Send Invite"]').click()
        print("- Submit invite form")

    def check_invitation(self, driver):
        self.delay(2)

        driver.find_element_by_xpath("//span[contains(text(), '" + self.email + "')]")
        print("- Check invitation success")

    def delay(self, second):
        time.sleep(second)

    def setup_driver(self):
        # setup headless and chromedriver
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')   
        chrome_driver = os.getcwd() + "/chromedriver" + self.driver_os()

        # setup selenium driver using chrome
        driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
        return driver

    def driver_os(self):
        os_type = platform.system()
        if os_type == "Linux":
            return "_linux"
        elif os_type == "Darwin":
            return "_mac"
        else:
            return ""
