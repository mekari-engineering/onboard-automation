from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import platform
import os
import time

class JenkinsProvider:
    LOGIN_URL="https://thor.sleekr.id/login"
    USERS_URL="https://thor.sleekr.id/securityRealm/addUser" 

    def __init__(self, username, full_name, email):
        self.username = username
        self.full_name = full_name
        self.email = email

    def onboard(self):
        driver = self.setup_driver()
        print("\n- Start onboarding Jenkins")

        try:
            self.sign_in(driver)
            self.create_user(driver)
            self.send_mailer()
            print("- Finish onboarding Jenkins")
        except Exception as e:
            print("- Error " + str(e))
        finally:
            driver.close()

    def sign_in(self, driver):
        # go to login page
        driver.get(self.LOGIN_URL)
        print("- Sign In Jenkins")

        # login here
        username_input = driver.find_element_by_name("j_username")
        username_input.send_keys(os.environ["JENKINS_USERNAME"].strip())
        print("- Filling username")

        password_input = driver.find_element_by_name("j_password")
        password_input.send_keys(os.environ["JENKINS_PASSWORD"].strip())
        print("- Filling password")

        driver.find_element_by_xpath("//input[@type='submit']").click()
        print("- Submit login form")

    def create_user(self, driver):
        driver.get(self.USERS_URL)
        print("- Visit create user page")

        self.delay(2)

        # fill form here
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(self.username)
        print("- Filling username with " + self.username)

        password_input = driver.find_element_by_name("password1")
        password_input.send_keys("mekariNumber1")
        print("- Filling password with mekariNumber1")

        password_conf_input = driver.find_element_by_name("password2")
        password_conf_input.send_keys("mekariNumber1")
        print("- Filling password confirmation with mekariNumber1")

        full_name_input = driver.find_element_by_name("fullname")
        full_name_input.send_keys(self.full_name)
        print("- Filling fullname with " + self.full_name)

        email_input = driver.find_element_by_name("email")
        email_input.send_keys(self.email)
        print("- Filling email with " + self.email)

        self.delay(2)

        # submit
        driver.find_element_by_xpath('//button[text()="Create User"]').click()
        print("- Submit create user form")

    def send_mailer(self):
        message = Mail(
            from_email='onboard-dev@mekari.com',
            to_emails=self.email,
            subject='Mekari Dev - Jenkins Credentials',
            html_content="""
	    Hi Mekarians,<br><br>

	    This is credentials for accessing jenkins<br><br>

	    URL: https://thor.sleekr.id<br>
	    Username: <b>{username}</b><br>
	    Password: <b>mekariNumber1</b><br><br>

	    Note: you need Pritunl VPN to access it, if you don't have please kindly request to DevOps team<br><br>

	    Thanks
            """.format(username=self.username))

	try:
	    sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"].strip())
	    response = sg.send(message)
	    print(response.status_code)
	    print(response.body)
	    print(response.headers)
	except Exception as e:
	    print("- Error " + str(e))

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
