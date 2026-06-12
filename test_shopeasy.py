import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


WEBSITE_URL = "https://mohdhussainnadaf.github.io/my-first-project-shop-easy/"


@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(WEBSITE_URL)
    yield driver
    driver.quit()


def wait_for(driver, locator):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(locator)
    )


def click_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    driver.execute_script("arguments[0].click();", element)


def test_valid_login(driver):
    wait_for(driver, (By.ID, "email")).send_keys("test@gmail.com")
    driver.find_element(By.ID, "password").send_keys("123456")

    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
    click_element(driver, login_button)

    message = wait_for(driver, (By.ID, "loginMessage")).text

    assert "Login successful" in message


def test_invalid_login(driver):
    wait_for(driver, (By.ID, "email")).send_keys("test@gmail.com")
    driver.find_element(By.ID, "password").send_keys("wrongpassword")

    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
    click_element(driver, login_button)

    message = wait_for(driver, (By.ID, "loginMessage")).text

    assert "Invalid email or password" in message


def test_search_valid_product(driver):
    search_box = wait_for(driver, (By.ID, "searchBox"))
    search_box.send_keys("Laptop")

    laptop = wait_for(driver, (By.XPATH, "//*[contains(text(), 'Laptop')]"))

    assert laptop.is_displayed()


def test_add_product_to_cart(driver):
    add_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Add to Cart')]"))
    )

    click_element(driver, add_buttons[0])

    cart_text = wait_for(driver, (By.ID, "cartItems")).text
    total = wait_for(driver, (By.ID, "total")).text

    assert "Laptop" in cart_text
    assert "45000" in total


def test_remove_product_from_cart(driver):
    add_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Add to Cart')]"))
    )

    click_element(driver, add_buttons[0])

    remove_button = wait_for(driver, (By.XPATH, "//button[contains(text(), 'Remove')]"))
    click_element(driver, remove_button)

    cart_text = wait_for(driver, (By.ID, "cartItems")).text
    total = wait_for(driver, (By.ID, "total")).text

    assert "Laptop" not in cart_text
    assert total == "0"


def test_checkout_with_valid_details(driver):
    add_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Add to Cart')]"))
    )

    click_element(driver, add_buttons[0])

    wait_for(driver, (By.ID, "customerName")).send_keys("Mohd Hussain Nadaf")
    driver.find_element(By.ID, "phone").send_keys("9876543210")
    driver.find_element(By.ID, "address").send_keys("Bengaluru, Karnataka")

    payment_dropdown = Select(driver.find_element(By.ID, "payment"))
    payment_dropdown.select_by_value("cod")

    place_order_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Place Order')]")
    click_element(driver, place_order_button)

    message = wait_for(driver, (By.ID, "orderMessage")).text

    assert "Order placed successfully" in message
