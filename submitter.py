#! python3
# submitter.py - Submits files to Momotor.

# --- Imports
from selenium.webdriver.chrome.options import Options

import os
from selenium import webdriver

# --- Get secrets from SECRET.
url = os.environ['URL']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
source_dir = os.environ['DIR']
files = os.environ['FILES'].split(',')

chrome_options = Options()
# chrome_options.add_argument("--headless")

# --- Initialize the WebDriver.
if os.name == 'posix':
    browser = webdriver.Chrome(options=chrome_options)
else:
    # Assume os.name == 'nt'
    browser = webdriver.Chrome(executable_path=r'chromedriver.exe', options=chrome_options)

browser.get(url)

# --- Sign in, if not signed in yet.
if browser.title == "Sign In":
    print("    Signing in...")
    browser.find_element_by_id("userNameInput").send_keys(username)
    browser.find_element_by_id("passwordInput").send_keys(password)
    browser.find_element_by_id("submitButton").click()
else:
    print("    Already signed in...")

# --- Submit files.
print("    Submitting", len(files), "files...")
try:
    browser.find_element_by_link_text("Submit Assignment").click()
except:
    browser.find_element_by_link_text("Re-submit Assignment").click()
for index, file in enumerate(files):
    browser.find_element_by_name("attachments[" + str(index) + "][uploaded_data]").send_keys(source_dir + file)
    browser.find_element_by_css_selector(".add_another_file_link").click()
browser.find_element_by_id("submit_file_button").click()

# --- Close the WebDriver.
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
