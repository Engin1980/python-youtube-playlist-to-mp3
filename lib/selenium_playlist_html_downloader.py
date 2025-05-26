from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

__verbose = True


def download_playlist_html(url: str, verbose: bool) -> str:
    global __verbose
    __verbose = verbose
    ret: str

    ret = __download_full_page(url)

    return ret


def __log(*args, **kwargs):
    if __verbose:
        print(*args, **kwargs)


def __scroll_to_bottom(driver, pause_time=2):
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


def __download_full_page(url, scroll_delay_seconds: int = 2, final_delay_seconds: int = 2):
    __log("Starting download of " + url)
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    service = Service()  # Automatically uses chromedriver if installed correctly

    __log("Opening page ...")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    __log("Opening page ... completed")

    __log("Accepting license ...")
    button = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Přijmout vše"]'))
        # TODO do internationally somehow
    )
    button.click()
    __log("Accepting license ... completed")

    __scroll_to_bottom(driver, scroll_delay_seconds)

    # Optional: wait for any last dynamic content to load
    time.sleep(final_delay_seconds)
    __log("Accepting license ... completed")

    print("Reading result ...")
    ret = driver.page_source
    driver.quit()
    print(f"Reading result ... completed, length: {len(ret)} characters")
    return ret


if __name__ == "__main__":
    # Example usage
    html_content = download_playlist_html("https://www.youtube.com/playlist?list=PLF273091A22D1723E", verbose=True)
    print(f"Downloaded HTML content length: {len(html_content)} characters")
