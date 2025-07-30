from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
import time


@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.get('https://the-internet.herokuapp.com/login')
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()

CredentialsX = [
    ('tomsmith','SUpermanWkwkw'),           # user ❌ pwd ✅
    ('tomnihahah','SuperSecretPassword!'),  # user ❌ pwd ✅
    ('tompleewkwkw','SUpermanWkwkw')        # user ❌ pwd ❌
    ]


@pytest.mark.negativetest
@pytest.mark.parametrize('q,w', CredentialsX)
def test_loginfailed(q,w,driver):
    driver.find_element(By.ID, 'username').send_keys(q)
    driver.find_element(By.ID, 'password').send_keys(w)
    driver.find_element(By.XPATH, '//*[@id="login"]/button/i').click()
    time.sleep(1)
    driver.get_screenshot_as_file('FailedLogin.png')
    error_text = driver.find_element(By.ID, 'flash').text.split('\n')[0].strip()
     # Cek kondisi username dan password
    if q != 'tomsmith' and w != 'SuperSecretPassword!':
        # Rrror → assert untuk salah satu yang mungkin
        assert error_text in [
            'Your username is invalid!',
            'Your password is invalid!'
        ]
    elif q != 'tomsmith':
        assert error_text == 'Your username is invalid!'
        driver.get_screenshot_as_file('FailedLogin1.png')
    elif w != 'SuperSecretPassword!':
        assert error_text == 'Your password is invalid!'
        driver.get_screenshot_as_file('FailedLogin2.png')

    driver.find_element(By.CLASS_NAME, 'close').click()
    time.sleep(1)
    # Click Login Without Fill User and Password
def test_loginovalue(driver):
    driver.find_element(By.XPATH, '//*[@id="login"]/button/i').click()
    driver.get_screenshot_as_file('FailedLogin3.png')
    time.sleep(1)
    print('Gagal Login')
    driver.find_element(By.CLASS_NAME, 'close').click()
    time.sleep(1)


@pytest.mark.positivetest
def test_loginsuccess(driver):
    driver.find_element(By.ID, 'username').send_keys('tomsmith')
    driver.find_element(By.ID, 'password').send_keys('SuperSecretPassword!')
    driver.find_element(By.XPATH, '//*[@id="login"]/button/i').click()
    time.sleep(1)
    driver.get_screenshot_as_file("SuccessLogin.png")
    LoginMessage = driver.find_element(By.ID, 'flash').text
    assert LoginMessage == 'You logged into a secure area!\n×'
    driver.find_element(By.CLASS_NAME, 'close').click()
    time.sleep(1)
    # Click Footer
    driver.find_element(By.XPATH, '//*[@id="page-footer"]/div/div/a').click()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(1)
    driver.get_screenshot_as_file("NewTab.png")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    # Logout
def test_logout(driver):
    driver.find_element(By.ID, 'username').send_keys('tomsmith')
    driver.find_element(By.ID, 'password').send_keys('SuperSecretPassword!')
    driver.find_element(By.XPATH, '//*[@id="login"]/button/i').click()
    driver.find_element(By.CLASS_NAME, 'close').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="content"]/div/a').click()
    time.sleep(1)
    driver.save_screenshot('Logout.png')
    LogoutMessage = driver.find_element(By.ID, 'flash').text
    assert LogoutMessage == 'You logged out of the secure area!\n×'
    print(LogoutMessage)
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'close').click()
    time.sleep(1)