import time
import re
import json

from urllib.parse import urljoin

from progress_bar import Progress_bar

import csv
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select




from selenium.webdriver.chrome.options import Options

URL = "https://www.homegate.ch/en"
LOCATION = "Lugano"
RADIUS = 10000
MAX_PRICE = 1000
ROOMS = 3.5

CSV = False
OUTPUT_FILE = 'apartments.csv'

BAR_WIDTH = 40

fieldnames = ['name', 'price', 'location', 'rooms', 'surface', 'desc']

apartments = []


def init_driver():
    options = Options()

    # Opciones de ventana
    options.add_argument("--start-maximized")

    # Ignorar errores de certificados
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.accept_insecure_certs = True

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

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



def try_get_element_text(parent, selector):
    out = None
    try:
        out = parent.find_element(By.CSS_SELECTOR, selector).text
    except:
        pass
    return out

def scrape_apartment (apartment_element):
    name = try_get_element_text(apartment_element, '.HgListingDescription_description_r5HCO > :nth-child(1)')

    desc = try_get_element_text(apartment_element, '.HgListingDescription_description_r5HCO > :nth-child(2)')

    location = try_get_element_text(apartment_element, 'address')

    price_text = try_get_element_text(apartment_element, '.HgListingCard_price_JoPAs')
    price = None
    if price is not None:
        price = float(re.search(r'\d+', price_text).group())

    rooms = try_get_element_text(apartment_element, '.HgListingRoomsLivingSpace_roomsLivingSpace_GyVgq > :nth-child(1) > strong')

    surface_text = try_get_element_text(apartment_element, '.HgListingRoomsLivingSpace_roomsLivingSpace_GyVgq > :nth-child(2) > strong')
    surface = None
    if surface_text is not None:
        surface = re.search(r'\d+', surface_text).group()

    return {
            'name': name,
            'price': price,
            'location': location,
            'rooms': rooms,
            'surface': surface,
            'desc': desc
        }

def full_scrape_apartment(driver):
    name=None
    desc=None
    location=None
    price=None
    rooms=None
    surface=None
    latitude=None
    longitude=None
    floor=None
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
        price_text = apartment_element.find_element(By.CSS_SELECTOR, '.HgListingCard_price_JoPAs').text
        price = float(re.search(r'\d+', price_text).group())
    except:
        pass
    try:
        rooms = apartment_element.find_element(By.CSS_SELECTOR, '.HgListingRoomsLivingSpace_roomsLivingSpace_GyVgq > :nth-child(1) > strong').text
    except:
        pass
    try:
        surface = re.search(r'\d+', apartment_element.find_element(By.CSS_SELECTOR, '.HgListingRoomsLivingSpace_roomsLivingSpace_GyVgq > :nth-child(2) > strong').text).group()
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

def full_scrape():
    apartments = []
    

    # Regex para sacar nº total de apartamentos
    print(driver.find_element(By.CSS_SELECTOR, ".searchButton .HgButton_content_RMjt_").text)
    total = int(re.search(r'\d+', driver.find_element(By.CSS_SELECTOR, ".searchButton .HgButton_content_RMjt_").text).group())
    
    progress_bar = Progress_bar(total = total)
    while True:

        apartments = driver.find_elements(By.CSS_SELECTOR, 'div[role=listitem] a')

        # Select the next page button if it exists
        next_button = None
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Go to next page"]')
        except Exception as e:
            next_button = None
            
        for apartment in apartments:

            link = urljoin(apartment.get_attribute('href'), URL)

            driver.get("")

            apartments.append(full_scrape_apartment(driver))
            
            progress_bar.increment()
            

        # Cycle to next page if there is
        if next_button is None:
            break
        time.sleep(1)
        next_button.click()
    print()
    return apartments

def fast_scrape():
    apartments = []
    

    # Regex para sacar nº total de apartamentos
    print(driver.find_element(By.CSS_SELECTOR, ".searchButton .HgButton_content_RMjt_").text)
    total = int(re.search(r'\d+', driver.find_element(By.CSS_SELECTOR, ".searchButton .HgButton_content_RMjt_").text).group())

    progress_bar = Progress_bar(total = total)

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
            
            progress_bar.increment()

        # Cycle to next page if there is
        if next_button is None:
            break
        time.sleep(1)
        next_button.click()
    print()
    return apartments


def dump_data(apartments):
    if CSV:
        with open(OUTPUT_FILE, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write the header (field names)
            writer.writeheader()
            
            # Write the data rows
            for apartment in apartments:
                writer.writerow(apartment)
    else:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(apartments, f, indent=4)

try:
    driver = init_driver()

    driver.get(URL)

    # Accept cookies
    cookie_button_accept = driver.find_element(by=By.CSS_SELECTOR, value="#onetrust-accept-btn-handler")
    cookie_button_accept.click()

    # Fill search filds and load list
    search()

    # Extract data
    apartments = fast_scrape()

except Exception as e:
    print()
    print("ERROR: ", e)

else:
    dump_data(apartments)

finally:
    driver.quit()

    

    
