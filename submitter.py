#! python3
# submitter.py - Submits files to Momotor.

# --- Importing imports. --- #
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import os, glob

# --- Get variables from ENV. --- #
url = os.environ['SUBMITTER_URL']
username = os.environ['SUBMITTER_USERNAME']
password = os.environ['SUBMITTER_PASSWORD']
source_dir = os.environ['SUBMITTER_DIR']
files = os.environ['SUBMITTER_FILES'].split(',')

# --- Initialize and set the WebDriver. --- #
chrome_options = Options()
chrome_options.add_argument("--headless")
if os.name == 'posix':
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options=chrome_options)
else:
    # Assume os.name == 'nt'
    browser = webdriver.Chrome(executable_path=r'chromedriver.exe', options=chrome_options)
browser.get(url)

# --- Simulate the submission. --- #

# Sign in, if not signed in yet.
if browser.title == "Sign In":
    print("    Signing in...")
    browser.find_element_by_id("userNameInput").send_keys(username)
    browser.find_element_by_id("passwordInput").send_keys(password)
    browser.find_element_by_id("submitButton").click()
else:
    print("    Already signed in...")

# Submit files.
all_files = []
for file in files:
    all_files.extend(glob.glob(source_dir+"\\"+file))
print("    Submitting", len(all_files), "files...")
WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'submit_assignment_link'))).click()
for index, file in enumerate(all_files):
    browser.find_element_by_name("attachments[" + str(index) + "][uploaded_data]").send_keys(file)
    browser.find_element_by_css_selector(".add_another_file_link").click()
browser.find_element_by_id("submit_file_button").click()

# Finish the submission by closing the WebDriver.
print("    Finishing submission...")
finished = False
try:
    WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'submit_assignment_link')))
    print("Submission finished!")
except TimeoutException:
    print("Submission failed!")
finally:
    browser.quit

# --- End. --- #
