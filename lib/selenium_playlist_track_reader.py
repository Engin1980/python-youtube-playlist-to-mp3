from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def scroll_to_bottom(driver, pause_time=2):
    print("Scrolling to the end ...")
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    counter = 1
    while True:
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.END)
        time.sleep(pause_time)
        print("\t " + str(counter) + " iteration")
        counter += 1
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        print(new_height)
        if new_height == last_height:
            break
        last_height = new_height

    print("Scrolling to the end ... completed")


def download_full_page(url, output_file="output.html"):
    print("Starting download of " + url)
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    service = Service()  # Automatically uses chromedriver if installed correctly

    print("Opening page ...")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    print("Opening page ... completed")

    print("Accepting license ...")
    button = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Přijmout vše"]'))
    )
    button.click()
    print("Accepting license ... completed")

    scroll_to_bottom(driver)

    # Optional: wait for any last dynamic content to load
    time.sleep(2)

    print("Saving result ...")
    html = driver.page_source
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    driver.quit()
    print(f"Saving result ... completed into: {output_file}")


# Example usage
download_full_page("https://www.youtube.com/playlist?list=PLF273091A22D1723E")
