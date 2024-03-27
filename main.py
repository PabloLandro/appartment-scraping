import time
import re
import json
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

BAR_WIDTH = 40

apartments = []


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

def scrape_apartment (apartment_element):
    name=None
    desc=None
    location=None
    price=None
    rooms=None
    surface=None
    try:
        name = apartment_element.find_element(By.CSS_SELECTOR, '.HgListingDescription_description_r5HCO > :nth-child(1)').text
    except:
        pass
    try:
        desc = apartment_element.find_element(By.CSS_SELECTOR, '.HgListingDescription_description_r5HCO > :nth-child(2)').text
    except:
        pass
    try:
        location = apartment_element.find_element(By.CSS_SELECTOR, 'address').text
    except:
        pass
    try:
        price = apartment_element.find_element(By.CSS_SELECTOR, '.HgListingCard_price_JoPAs').text
    except:
        pass
    try:
        rooms = apartment_element.find_element(By.CSS_SELECTOR, '.HgListingRoomsLivingSpace_roomsLivingSpace_GyVgq > :nth-child(1) > strong').text
    except:
        pass
    try:
        surface = apartment_element.find_element(By.CSS_SELECTOR, '.HgListingRoomsLivingSpace_roomsLivingSpace_GyVgq > :nth-child(2) > strong').text
    except:
        pass
    return {
            'name': name,
            'price': price,
            'location': location,
            'rooms': rooms,
            'surface': surface,
            'desc': desc
        }


def scrape():
    apartments = []
    

    # Regex para sacar nº total de apartamentos
    print(driver.find_element(By.CSS_SELECTOR, ".searchButton .HgButton_content_RMjt_").text)
    total = int(re.search(r'\d+', driver.find_element(By.CSS_SELECTOR, ".searchButton .HgButton_content_RMjt_").text).group())
    idx = 0    
    while True:

        apartment_elements = driver.find_elements(By.CSS_SELECTOR, 'div[role=listitem]')

        # Select the next page button if it exists
        next_button = None
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Go to next page"]')
        except Exception as e:
            next_button = None
            
        for apartment_element in apartment_elements:
            
            apartments.append(scrape_apartment(apartment_element))
            idx += 1
            # Progress bar
            progress = int((idx) / total * BAR_WIDTH)
            bar = '[' + '#' * progress + ' ' * (BAR_WIDTH - progress) + ']'
            print(f'\r{bar} {idx}/{total} apartments screaped', end='', flush=True)

        # Cycle to next page if there is
        if next_button is None:
            break
        next_button.click()
    print()
    return apartments


try:
    driver = init_driver()

    driver.get(URL)

    # Accept cookies
    cookie_button_accept = driver.find_element(by=By.CSS_SELECTOR, value="#onetrust-accept-btn-handler")
    cookie_button_accept.click()

    search()

    apartments = scrape()

except Exception as e:
    print("ERROR: ", e)

else:
    with open('apartments.json', 'w') as f:
        json.dump(apartments, f, indent=4)

finally:
    driver.quit()

    

    
