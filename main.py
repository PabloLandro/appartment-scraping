import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select




from selenium.webdriver.chrome.options import Options

URL = "https://www.homegate.ch/en"
LOCATION = "Lugano"
RADIUS = 10000
MAX_PRICE = 1000
ROOMS = 3.5




def init_driver():
    options = Options()

    # Opciones de ventana
    options.add_argument("--start-maximized")

    # Ignorar errores de certificados
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.accept_insecure_certs = True

    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(2)
    return driver

def set_dropdown(driver, name, value):
    dropdown = Select(driver.find_element(by=By.CSS_SELECTOR, value="select[name=" + str(name) + "]"))
    dropdown.select_by_value(str(value))

def search():

    # Input LOCATION
    location_box = driver.find_element(by=By.CSS_SELECTOR, value=".Locations_locationsWrapper_X0H6J")
    location_box.click()

    location_input = driver.find_element(by=By.CSS_SELECTOR, value="input[name=locations]")
    location_input.send_keys(LOCATION)

    location_options = driver.find_element(by=By.CSS_SELECTOR, value=".Locations_itemsHolder_KXmeo")
    first_option = location_options.find_element(by=By.CSS_SELECTOR, value=":first-child")
    first_option.click()

    driver.find_element(by=By.CSS_SELECTOR, value="html").click()

    # Input RADIUS
    set_dropdown(driver, "radius", RADIUS)

    # Input MAX_PRICE
    set_dropdown(driver, "price", MAX_PRICE)

    # Input Rooms
    set_dropdown(driver, "rooms", ROOMS)

    search_button = driver.find_element(by=By.CSS_SELECTOR, value="button[data-cy=SearchBar_button]")
    search_button.click()

try:
    driver = init_driver()

    driver.get(URL)

    # Accept cookies
    cookie_button_accept = driver.find_element(by=By.CSS_SELECTOR, value="#onetrust-accept-btn-handler")
    cookie_button_accept.click()

    search()

    

finally:
    time.sleep(2)
    driver.quit()
