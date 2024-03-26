import time
from selenium import webdriver
from selenium.webdriver.common.by import By


from selenium.webdriver.chrome.options import Options

try:
    options = Options()
    options.add_argument("--start-maximized")

    # Ignorar errores de certificados
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.accept_insecure_certs = True

    driver = webdriver.Chrome(options=options)

    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

    text_input = driver.find_element(by=By.CSS_SELECTOR, value="#my-text-id")
    text_input.send_keys("Selenium")


finally:
    time.sleep(2)
    driver.quit()
