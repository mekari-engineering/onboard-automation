from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import platform
import os
import time

class PapertrailProvider:
    LOGIN_URL="https://my.solarwinds.cloud/login?client_id=papertrail&redirect_uri=https%3A%2F%2Fpapertrailapp.com%2Faccount%2Fauth%2Fswicus%2Fcallback&response_type=code&scope=openid+swicus&state=q96tRqGAiNlq8AlqE0KfDuzT68CF%2FM%2Fu%2Bll%2B4LYy9NM%3D"
    INVITE_URL="https://papertrailapp.com/members/new"

    def __init__(self, email):
        self.email = email

    def onboard(self):
        driver = self.setup_driver()
        print("\n- Start onboarding Papertrail")

        try:
            self.sign_in(driver)
            self.invite_user(driver)
            self.check_invitation(driver)
            print("- Finish onboarding Papertrail")
        except Exception as e:
            print("- Error " + str(e))
        finally:
           driver.close()

    def sign_in(self, driver):
        driver.get(self.LOGIN_URL)
        print("- Sign In Papertrail")
        
        email_input = driver.find_element_by_name("email")
        email_input.send_keys(os.environ["PAPERTRAIL_USERNAME"].strip())
        print("- Filling username")

        password_input = driver.find_element_by_name("password")
        password_input.send_keys(os.environ["PAPERTRAIL_PASSWORD"].strip())
        print("- Filling password")

        driver.find_element_by_xpath('//button[text()="Log in"]').click()
        print("- Submit login form")
    
    def invite_user(self, driver):
        self.delay(2)

        driver.get(self.INVITE_URL)
        print("- Visit invite page")

        self.delay(2)
        
        email_input = driver.find_element_by_id("email")
        email_input.send_keys(self.email)
        print("- Invite email " + self.email)

        manage_member_checkbox = driver.find_element_by_name("members[][manage_members]")
        manage_member_checkbox.click()
        print("- Untick 'Manage users and permissions' field")

        self.delay(2)

        manage_billing_checkbox = driver.find_element_by_name("members[][manage_billing]")
        manage_billing_checkbox.click()
        print("- Untick 'Change plans and payment' field")

        receive_usage_emails_checkbox = driver.find_element_by_name("members[][receive_usage_emails]")
        receive_usage_emails_checkbox.click()
        print("- Untick 'Usage' field")

        receive_billing_emails_checkbox = driver.find_element_by_name("members[][receive_billing_emails]")
        receive_billing_emails_checkbox.click()
        print("- Untick 'Billing' field")

        driver.find_element_by_xpath('//button[contains(text(), "Invite Member")]').click()
        print("- Submit invite form")

    def check_invitation(self, driver):
        self.delay(2)

        driver.find_element_by_xpath("//p[contains(text(), '" + self.email + " was sent a warm invitation')]")
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
