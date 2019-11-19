from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import platform
import os
import time

class SentryProvider:
    LOGIN_URL="https://sentry.io/auth/login/"
    INVITE_URL="https://sentry.io/settings/pt-jurnal-consulting-indonesia/members/"

    def __init__(self, email):
        self.email = email

    def onboard(self):
        driver = self.setup_driver()
        print("\n- Start onboarding Sentry")

        try:
            self.sign_in(driver)
            self.invite_user(driver)
            self.check_invitation(driver)
            print("- Finish onboarding Sentry")
        except Exception as e:
            print("- Error " + str(e))
        finally:
           driver.close()

    def sign_in(self, driver):
        driver.get(self.LOGIN_URL)
        print("- Sign In Sentry")
        
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(os.environ["SENTRY_USERNAME"].strip())
        print("- Filling username")

        password_input = driver.find_element_by_name("password")
        password_input.send_keys(os.environ["SENTRY_PASSWORD"].strip())
        print("- Filling password")

        driver.find_element_by_xpath('//button[text()="Continue"]').click()
        print("- Submit login form")
    
    def invite_user(self, driver):
        self.delay(2)

        driver.get(self.INVITE_URL)
        print("- Visit invite page")

        self.delay(3)

        driver.find_element_by_xpath('//span[contains(text(), "Invite Members")]').click()

        self.delay(1)
        
        email_input = driver.find_element_by_xpath("//input[@aria-activedescendant='react-select-2--value']")
        email_input.send_keys(self.email)
        print("- Invite email " + self.email)

        driver.find_element_by_xpath('//p[contains(text(), "Invite new members by email to join your organization.")]').click()

        self.delay(2)

        driver.find_element_by_xpath('//span[contains(text(), "Send invite")]').click()
        print("- Submit invite form")

    def check_invitation(self, driver):
        self.delay(3)

        driver.find_element_by_xpath("//strong[contains(text(), '1 invite')]")
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
