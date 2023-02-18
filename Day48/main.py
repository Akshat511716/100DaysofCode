import time
from selenium import webdriver
from selenium.webdriver.common.by import By

PAGE_URL = "http://orteil.dashnet.org/experiments/cookie/"
# amount of time for the clicker to run, in seconds
TIMEOUT = 300
# amount of time between checking for upgrades, in seconds
CHECK_INTERVAL = 15


def buy_upgrade():
    """Purchases the most expensive available upgrade."""
    # get current number of cookies
    raw_cookies = driver.find_element(By.ID, "money").text
    # remove the possible period
    cookies = int(raw_cookies.replace(",", ""))

    # get current prices for each upgrade
    raw_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
    # using list comprehension to extract only the price part
    prices = [int(price.text.split("-")[1].strip().replace(",", "")) for price in raw_prices if price.text != ""]

    # dictionary with upgrades and prices
    upgrades = {}
    for n in range(len(prices)):
        upgrades[prices[n]] = item_ids[n]

    # find purchasable upgrades
    purchasable_upgrades = {}
    for upgrade_cost, upgrade_id in upgrades.items():
        if cookies > upgrade_cost:
            purchasable_upgrades[upgrade_cost] = upgrade_id

    # click on the most expensive purchasable upgrade
    driver.find_element(By.ID, purchasable_upgrades[max(purchasable_upgrades)]).click()


driver = webdriver.Firefox()
driver.get(PAGE_URL)
cookie = driver.find_element(By.ID, "cookie")

# get store items
item_list = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in item_list]

# set timers
start_time = time.time()
end_time = start_time + TIMEOUT
check_time = start_time + CHECK_INTERVAL

while time.time() < end_time:
    # click with each iteration
    cookie.click()
    # check for upgrades after the set about of time
    if time.time() > check_time:
        buy_upgrade()
        # time for the next the next check
        check_time += CHECK_INTERVAL

cps = driver.find_element(By.ID, "cps").text
print(f"Exited after {TIMEOUT} seconds with a score of {cps.split(' : ')[1]} cookies per second.")

driver.close()
