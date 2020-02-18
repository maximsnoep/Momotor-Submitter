#! python3
# submitter.py - Submits files to Momotor.

# --- Imports
import SECRET
from selenium import webdriver

# --- Get secrets from SECRET.
URL = SECRET.URL;
USERNAME = SECRET.USERNAME;
PASSWORD = SECRET.PASSWORD;
DIR = SECRET.DIR;
FILES = SECRET.FILES;

# --- Initialize the WebDriver.
browser = webdriver.Chrome(executable_path=r'chromedriver.exe');
browser.get(URL);

# --- Sign in, if not signed in yet.
if browser.title == "Sign In":
    print("    Signing in...")
    browser.find_element_by_id("userNameInput").send_keys(USERNAME)
    browser.find_element_by_id("passwordInput").send_keys(PASSWORD)
    browser.find_element_by_id("submitButton").click()
else:
    print("    Already signed in...")

# --- Submit files.
print("    Submitting", len(FILES), "files...")
try:
    browser.find_element_by_link_text("Submit Assignment").click()
except:
    browser.find_element_by_link_text("Re-submit Assignment").click()
for index, file in enumerate(FILES):
    browser.find_element_by_name("attachments[" + str(index) + "][uploaded_data]").send_keys(DIR + file)
    browser.find_element_by_css_selector(".add_another_file_link").click()
browser.find_element_by_id("submit_file_button").click()

# --- Close the WebDriver.
print("    Finishing submission...")
finished = False;
while not finished:
    try:
        browser.find_element_by_link_text("Re-submit Assignment")
        browser.quit();
        finished = True;
    except:
        pass;
print("Submission finished!")
