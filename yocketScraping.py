from selenium.common.exceptions import StaleElementReferenceException

YOCKET_PATH = 'https://yocket.in'
USERNAME = 'moharsuperleo95@gmail.com'
PASSWORD = 'abcd2314'
text = '/profiles/find/matching-admits-and-rejects'
# Selenium works when all elements on the page is loaded

from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
import json

# Options
options = webdriver.ChromeOptions()
options.add_argument('--incognito')

# WebDriverPath
browser = webdriver.Chrome('/home/debadatta/ML_learning_Path/Data_Science_and_ML_Projects/yocketScraping/chromedriver',
                           chrome_options=options)

page = 0

detailOfAllStudent = []

# maximuize the window
browser.maximize_window()

# Yocket link
browser.get(YOCKET_PATH)

time.sleep(3)

# Find email input
uname = browser.find_element_by_id('email')
time.sleep(2)
uname.send_keys(USERNAME)

# Find NextButton
browser.find_element_by_id('users_login_email').click()
time.sleep(2)

# Find Password Input
password = browser.find_element_by_id('password')
time.sleep(2)
password.send_keys(PASSWORD)

# Click on Sign IN button
browser.find_element_by_id('users_login_password').click()
time.sleep(2)
print('Login Successful')

# Click on Services DropDown
ul = browser.find_elements_by_xpath(
    '//*[@class="navbar navbar-default navbar-fixed-top yamm hidden-xs"]//div[@class="row"]//div[@class="col-md-12"]//div[@class="navbar-collapse collapse"]//ul//li[@class="dropdown yamm-fw"]')[
    2].click()

time.sleep(3)

# Click on Admit and Rejects
browser.find_element_by_xpath(
    '//*[@id="navbar-collapse-grid"]/ul/li[5]/ul/li/div/div[1]/ul/li[7]/a').click()
time.sleep(2)

# Get Page Source
pageSource = browser.page_source

# Beautiful Soup
soup = BeautifulSoup(pageSource, 'lxml')


def getDetailsOfAllStudents(panelBody):
    studentDetails = {}
    for panels in panelBody:
        nameCollegeandUni = panels.find('div', class_='row')
        name = nameCollegeandUni.find('div', class_='col-sm-9').find('a').get_text()
        status = nameCollegeandUni.find('div', class_='col-sm-3 text-uppercase').find('label').get_text()
        college = nameCollegeandUni.find('div', class_='col-sm-9').find('small').get_text().split('\n')[1]
        yearInterested = nameCollegeandUni.find('div', class_='col-sm-9').find('small').get_text().split('\n')[2]
        details = panels.find('div', class_='row text-center')
        greToeflUndergradWorkExp = details.find_all('div', class_='col-sm-3 col-xs-6')
        greGmat = {'gregmat': greToeflUndergradWorkExp[0].text.split('\n')[1],
                   'score': greToeflUndergradWorkExp[0].text.split('\n')[2]}
        toeflIelts = {'toelfIelts': greToeflUndergradWorkExp[1].text.split('\n')[1],
                      'score': greToeflUndergradWorkExp[1].text.split('\n')[2]}
        underGradMarks = greToeflUndergradWorkExp[2].text.split('\n')[2]
        workExperience = {'workExperience': greToeflUndergradWorkExp[3].text.split('\n')[1],
                          'score': greToeflUndergradWorkExp[3].text.split('\n')[2]}
        studentDetails = {
            'name': name,
            'college': college,
            'yearInterested': yearInterested,
            'undergradMarks': underGradMarks,
            'greOrGmatScore': greGmat,
            'toeflIeltsScore': toeflIelts,
            'workExperience': workExperience,
            'status': status
        }
        detailOfAllStudent.append(studentDetails)
    savetofile(detailOfAllStudent)
    print(detailOfAllStudent)
    clickButton()


def clickButton():
    if browser.find_element_by_class_name('fa-chevron-right'):
        browser.find_element_by_class_name('fa-chevron-right').click()
        checkNextButtonExits()


def checkNextButtonExits():
    browser.implicitly_wait(30)
    pageSource = browser.page_source
    soup = BeautifulSoup(pageSource, 'lxml')
    panelBody = soup.find_all('div', class_='panel-body')
    getDetailsOfAllStudents(panelBody)


def savetofile(data):
    f = open('details.json', 'w')
    json.dump(data, f, indent=4)
    f.close()


# Finding the small square panel body where data is stored.
panelBody = soup.find_all('div', class_='panel-body')
getDetailsOfAllStudents(panelBody)

print(detailOfAllStudent)
