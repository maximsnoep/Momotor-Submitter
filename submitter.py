#! python3
# submitter.py - Submits files to Momotor.

# --- Importing imports. --- #
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os

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
print("    Submitting", len(files), "files...")
try:
    browser.find_element_by_link_text("Submit Assignment").click()
except:
    browser.find_element_by_link_text("Re-submit Assignment").click()
for index, file in enumerate(files):
    browser.find_element_by_name("attachments[" + str(index) + "][uploaded_data]").send_keys(source_dir + file)
    browser.find_element_by_css_selector(".add_another_file_link").click()
browser.find_element_by_id("submit_file_button").click()

# Finish the submission by closing the WebDriver.
print("    Finishing submission...")
finished = False
while not finished:
    try:
        browser.find_element_by_link_text("Re-submit Assignment")
        browser.quit()
        finished = True
    except:
        pass
print("Submission finished!")

# --- End. --- #
