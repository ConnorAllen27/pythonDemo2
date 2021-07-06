import datetime
import os
from selenium.webdriver import DesiredCapabilities
import names
#from test_functions import *
import random
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from datetime import date
import pathlib
# from createMAData import *


#currentDirectory = str(pathlib.Path().absolute())


# Initiate the Driver instance with Zelenium
options = webdriver.ChromeOptions()
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
capabilities = {}
capabilities = DesiredCapabilities.CHROME.copy()

driver = webdriver.Remote(desired_capabilities=capabilities,
                          command_executor="http://34.152.9.236:4444/wd/hub",
                          options=options)

# driver = webdriver.Chrome(executable_path=str(pathlib.Path().absolute()) + "\\chromedriver.exe") # local driver
driver.implicitly_wait(10)

# Login into the MedAccess instance.
driver.get("https://dwgcppoc.emrlab.ca/auth/login.do")
driver.find_element_by_css_selector("input[name='username']").send_keys("medaccess")
driver.find_element_by_css_selector("input[id='pwdEntry']").send_keys("Telus2020!")
driver.find_element_by_css_selector("a[id='LoginButton']").click()
driver.maximize_window()

# To turn off the concealed mode
driver.switch_to.frame(0)
driver.switch_to.frame("Dashboard")
profile = driver.find_element_by_css_selector("div[title='Update User Profile']")
action = ActionChains(driver)
action.context_click(profile).context_click().perform()
driver.find_element_by_xpath("//li[@class='yuimenuitem'][1]").click()
time.sleep(1)

# Click on the search patient icon
driver.find_element_by_css_selector("div[title='Patient Search (S)']").click()
driver.switch_to.default_content()

# Click on the new patient icon
windows = driver.window_handles
newwindow = windows[1]
driver.switch_to.window(newwindow)
driver.maximize_window()
driver.find_element_by_css_selector("div[title='New Patient']").click()

# Switch to the window before adding patient demographics details
windows = driver.window_handles
newwindow = windows[1]
driver.switch_to.window(newwindow)
driver.maximize_window()

# Add patient demographics details_Identification.
lastName = names.get_last_name()
driver.find_element_by_css_selector("input[id='lastName']").send_keys(lastName)

driver.find_element_by_css_selector("input[id='firstName']").send_keys(names.get_first_name())
driver.find_element_by_css_selector("input[id='dob']").click()

# calculate random DOB
start_date = datetime.date(1940, 1, 1)
end_date = datetime.date(2020, 2, 1)
time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days
random_number_of_days = random.randrange(days_between_dates)
random_date = start_date + datetime.timedelta(days=random_number_of_days)
DOB = random_date.strftime("%d-%b-%Y")
driver.find_element_by_css_selector("input[id='dob']").send_keys(DOB)
driver.find_element_by_css_selector("input[id='firstName']").click()

gender = ["Unknown", "Female", "Male", "Other"]
genderValue = random.choice(gender)
dropdown = Select(driver.find_element_by_css_selector("select[id='gender']"))
dropdown.select_by_visible_text(genderValue)

maritalStatus = ["Annulled", "Common-law", "Divorced", "Domestic Partner", "Interlocutory", "Living Together",
                 "Married", "Other", "Separated", "Single", "Unknown", "Widowed"]
maritalStatusValue = random.choice(maritalStatus)
dropdown = Select(driver.find_element_by_css_selector("select[name*='.maritalStatusCode']"))
dropdown.select_by_visible_text(maritalStatusValue)

identifierGroup = ["Canadian Forces Number"]
identifierGroupValue = random.choice(identifierGroup)
identifierTypeGroup = Select(driver.find_element_by_xpath("//select[@name='identifierTypeGroupCode']"))
identifierTypeGroup.select_by_visible_text(identifierGroupValue)

identifierNumber = random.randint(100000000, 999999999)
driver.find_element_by_xpath("//input[@id='phnNumber']").send_keys(identifierNumber)

# Add patient demographics details_Address and Phone.
address = ["SlaterStreet", "LisgarStreet", "BankStreet", "GoodStreet", "BadStreet"]
addressValue = random.choice(address)
today = date.today()
todayDate = today.strftime("%Y%m%d")
driver.find_element_by_css_selector("input[name='patientData.address.address']").send_keys(addressValue)

city = ["ottawa", "Edmonton", "Vancouver", "Toronto"]
cityValue = random.choice(city)
driver.find_element_by_css_selector("input[name*='city']").send_keys(cityValue)

province = ["Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador",
            "Northwest Territories", "Nova Scotia", "Nunavut", "Ontario", "Prince Edward Island", "Quebec (PQ)",
            "Quebec (QC)", "Saskatchewan"]
provinceValue = random.choice(province)
dropdown = Select(driver.find_element_by_css_selector("select[name*='.provinceCode']"))
dropdown.select_by_visible_text(provinceValue)

postalCode = ["K1R 1A1", "K1R 2A2", "K1R 3A3", "K1R 4A4", "K1R 5A5", "K1R 6A6", "K1R 7A7", "K1R 8A8", "K1R 9A9"]
postalCodeValue = random.choice(postalCode)
driver.find_element_by_css_selector("input[name*='.postalCode']").send_keys(postalCodeValue)

addressTypeGroup = ["Home - Mailing", "Home - Permanent", "Business - Mailing", "Business - Permanent", "Other"]
addressTypeGroupValue = random.choice(addressTypeGroup)
dropdown = Select(driver.find_element_by_xpath("//select[@name='addressTypeGroupCode']"))
dropdown.select_by_visible_text(addressTypeGroupValue)

areaCode = random.randint(100, 999)
driver.find_element_by_css_selector("input[name*='[0].areaCode']").send_keys(areaCode)
number = random.randint(1000000, 9999999)
driver.find_element_by_css_selector("input[name*='[0].number']").send_keys(number)
ext = random.randint(100, 999)
driver.find_element_by_css_selector("input[name*='[0].extension']").send_keys(ext)

phoneTypeGroup = ["Home - Beeper", "Home - Cell", "Home - Fax", "Home - Phone", "Work - Beeper", "Work - Cell"]
phoneTypeGroupValue = random.choice(phoneTypeGroup)
dropdown = Select(driver.find_element_by_css_selector("select[name*='Code[0]']"))
dropdown.select_by_visible_text(phoneTypeGroupValue)

# Add patient demographics details_Care Assignments & Notes.
primaryProviderValue = random.choice(["Bishop, Kate", "Blue, Evan"])
dropdown = Select(driver.find_element_by_css_selector("select[name*='.primary']"))
dropdown.select_by_visible_text(primaryProviderValue)

secondaryProviderValue = random.choice(["Bishop, Kate", "Blue, Evan"])
dropdown = Select(driver.find_element_by_css_selector("select[name*='secondary']"))
dropdown.select_by_visible_text(secondaryProviderValue)

providerGroupValue = random.choice(["Shiv Kelly", "Canada Best", "Seashore Clinic"])
dropdown = Select(driver.find_element_by_css_selector("select[name*='userGroupId']"))
dropdown.select_by_visible_text(providerGroupValue)

familyProviderValue = random.choice(["Bishop, Kate", "Blue, Evan"])
driver.find_element_by_xpath("//input[@id='familyProviderValue']").clear()
driver.find_element_by_xpath("//input[@id='familyProviderValue']").send_keys(familyProviderValue)
driver.find_element_by_xpath("(//div[contains(@id,'provider')])[2]").click()

windows = driver.window_handles
newwindow = windows[2]
driver.switch_to.window(newwindow)
driver.maximize_window()

provinceTypeCount = len(driver.find_elements_by_xpath("(//div[@id='criteriaValue'])[3]"))
if provinceTypeCount > 0:
    driver.find_element_by_xpath("//select[contains(@name,'provinceCode')]/following-sibling::div").click()
    time.sleep(1)
    driver.find_element_by_xpath(
        "//div[@class='optionWrapper']/div[@class='criteriaOption'] //span[text()='All']").click()
    time.sleep(1)
else:
    dropdown = Select(driver.find_element_by_xpath("//select[contains(@name,'provinceCode')]"))
    dropdown.select_by_visible_text("All")

driver.find_element_by_xpath("//input[@id='searchButton']").click()
time.sleep(2)
driver.find_element_by_xpath("(//div[@id='providerSearchResults']/table/tbody/tr/td/a)[1]/table/tbody").click()
time.sleep(2)
windows = driver.window_handles
newwindow = windows[1]
driver.switch_to.window(newwindow)
driver.maximize_window()
driver.find_element_by_css_selector("input[id='updatePatient']").click()

# Grab patient id
time.sleep(4)
windows = driver.window_handles
newwindow = windows[1]
driver.switch_to.window(newwindow)
driver.maximize_window()
PatientID = driver.current_url
PatientID = PatientID[-5:]
print(PatientID)
driver.quit()

file = open('case_1//pInfo.txt','w')
file.write("id:" + PatientID +"\n")
file.write("addressValue:"+addressValue+"\n")
file.write("postalCodeValue:"+postalCodeValue+"\n")
file.write("provinceValue:"+provinceValue+"\n")
file.write("cityValue:"+cityValue+"\n")
file.write("DOB:"+DOB+"\n")
file.write("areaCode:"+str(areaCode)+"\n")
file.write("number:"+str(number)+"\n")
file.write("ext:"+str(ext)+"\n")
file.write("primaryProviderValue:"+primaryProviderValue+"\n")
file.write("secondaryProviderValue:"+secondaryProviderValue+"\n")
file.write("familyProviderValue:"+familyProviderValue+"\n")
file.close()


#time.sleep(30)
#time.sleep(300)




