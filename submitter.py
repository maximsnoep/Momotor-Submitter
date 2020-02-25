#! python3
# submitter.py - Submits files to Momotor.

# Imports
import sys, os, glob
from urllib.parse import urlparse
from selenium import webdriver

USERNAME = "username"   # Canvas username
PASSWORD = "password"   # Canvas password
DIR = os.getcwd()       # Get cwd
ARGUMENTS = sys.argv    # Get arguments

# First given argument should be the URL
if len(ARGUMENTS) < 2:
    print("Please provide a URL to the submission page! \nsubmittor [URL] [FILES](optional)")
    quit()
temp_url = urlparse(ARGUMENTS[1])
if temp_url[1] == "":
    print("Please provide a URL to the submission page! \nsubmittor [URL] [FILES](optional)")
    quit()
URL = temp_url[0]+temp_url[1]+temp_url[2]

# Other optional given arguments should be files
FILES = []
if ARGUMENTS[2] is not None:
    for i in range(2, len(ARGUMENTS)):
        temp_files = glob.glob(DIR+"/"+ARGUMENTS[i])
        for temp_file in temp_files:
            FILES.append(temp_file)
else:
    FILES.append(glob.glob(DIR+"/"+"*"))

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
    browser.find_element_by_name("attachments[" + str(index) + "][uploaded_data]").send_keys(file)
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
