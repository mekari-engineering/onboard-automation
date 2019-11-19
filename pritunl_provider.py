from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
import urllib2 as urllib
import platform
import os
import time
import base64
import json
import glob

class PritunlProvider:
    LOGIN_URL="https://vpn.sleekr.id/login"
    USERS_URL="https://vpn.sleekr.id/#/users"

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def onboard(self):
        driver = self.setup_driver()
        print("\n- Start onboarding Pritunl")

	try:
            self.cleanup_tar_files()
	    self.sign_in(driver)
	    self.create_user(driver)
	    self.download_vpn_profile(driver)
            self.send_mailer()
	    print("- Finish onboarding Pritunl")
	except Exception as e:
	    print("- Error " + str(e))
	finally:
	    driver.close()

    def cleanup_tar_files(self):
        print("- Cleanup tar files")

        for tar_file in self.list_tar_files():
	    if os.path.exists(tar_file):
	        os.remove(tar_file)

    def sign_in(self, driver):
        # go to login page
        driver.get(self.LOGIN_URL)
        print("- Sign In Pritunl")

        # login here
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(os.environ["VPN_USERNAME"].strip())
        print("- Filling username")

        password_input = driver.find_element_by_name("password")
        password_input.send_keys(os.environ["VPN_PASSWORD"].strip())
        print("- Filling password")

        driver.find_element_by_xpath("//input[@type='submit']").click()
        print("- Submit login form")

    def create_user(self, driver):
        self.delay(1)

        driver.get(self.USERS_URL)
        print("- Visit create user page")

        self.delay(1)

        # fill form here
        driver.find_element_by_css_selector('button.orgs-add-user').click()
        print("- Opening create user modal form")

        self.delay(1)

        username_input = driver.find_element_by_xpath("//input[@placeholder='Enter name']")
        username_input.send_keys(self.username)
        print("- Filling username with " + self.username)

        email_input = driver.find_element_by_xpath("//input[@placeholder='Enter email address']")
        email_input.send_keys(self.email)
        print("- Filling email with " + self.email)

        driver.find_element_by_css_selector('button.btn.btn-primary.ok').click()
        print("- Submit create user form")

    def download_vpn_profile(self, driver):
        self.delay(3)

        search_input = driver.find_elements_by_xpath("//input[@placeholder='Search for user']")[0]
        search_input.send_keys(self.username.replace(" ", ""))
        print("- Filter new created user")

        self.delay(3)

        download_link = driver.find_elements_by_css_selector('a.download-key.glyphicon.glyphicon-download.no-select')[0]
        driver.get(download_link.get_attribute("href"))
        print("- Download vpn profile")

        # wait download to finish
        self.delay(5)

    def send_mailer(self):
        message = Mail(
            from_email='onboard-dev@mekari.com',
            to_emails=self.email,
            subject='Mekari Dev - Pritunl VPN profile',
            html_content="""
            Hi Mekarians,<br><br>

            Here attachment for Pritunl VPN<br><br>
            
            Thanks
            """)

	message.attachment = self.file_attachment("seiko.tar")

        try:
            sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"].strip())
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print("- Error " + str(e))

    def file_attachment(self, file_name):
        file_path = self.list_tar_files()[0]
        with open(file_path, 'rb') as f:
	    data = f.read()
	    f.close()
	encoded = base64.b64encode(data).decode()
	attachment = Attachment()
	attachment.file_content = FileContent(encoded)
	attachment.file_type = FileType('application/x-tar')
	attachment.file_name = FileName('pritunl.tar')
	attachment.disposition = Disposition('attachment')
	attachment.content_id = ContentId('Example Content ID')
	return attachment

    def list_tar_files(self):
        return glob.glob(os.getcwd() + "/*.tar")

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
