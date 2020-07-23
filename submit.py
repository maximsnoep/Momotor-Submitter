#! python3
# submit.py - submits files to canvas.

# imports
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import os


# submit to canvas selenium script
def submit_to_canvas(url, username, password, files):
    # initializing the WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    if os.name == 'posix':
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        browser = webdriver.Chrome(options=chrome_options)
    else:
        browser = webdriver.Chrome(executable_path=r'utils/chromedriver.exe', options=chrome_options)

    # go to the url
    browser.get(url)

    # sign in if not signed in yet else continue
    if browser.title == "Sign In":
        print("    Signing in...")
        browser.find_element_by_id("userNameInput").send_keys(username)
        browser.find_element_by_id("passwordInput").send_keys(password)
        browser.find_element_by_id("submitButton").click()
    else:
        print("    Already signed in...")

    # submit files
    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'submit_assignment_link'))).click()
    # accept alert when assignment is overdue
    try:
        browser.switch_to.alert.accept()
    except:
        pass
    # actually submitting the files
    print("    Submitting", len(files), "files...")
    for i in range(len(files)):
        browser.find_element_by_name("attachments[" + str(i) + "][uploaded_data]").send_keys(files[i])
        browser.find_element_by_css_selector(".add_another_file_link").click()
    browser.find_element_by_id("submit_file_button").click()

    # finish the submission by closing the WebDriver
    print("    Finishing submission...")
    try:
        WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'submit_assignment_link')))
        print("Submission finished!")
    except TimeoutException:
        print("Submission failed!")
    finally:
        browser.quit()
