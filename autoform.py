from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  
from webdriver_manager.chrome import ChromeDriverManager
import time

# Poprawna inicjalizacja WebDriver z Service
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Otwieramy stronę https://www.python.org/
driver.get("http://127.0.0.1:5000/dodaj-zgloszenie")
time.sleep(2)

email = driver.find_element(By.NAME, 'email')
password = driver.find_element(By.NAME, 'password')

email.send_keys('admin@admin.admin')
password.send_keys('QWERTY1234!')


submit_button = driver.find_element(By.ID,'przycisk')
submit_button.click()
time.sleep(1)
driver.get("http://127.0.0.1:5000/dodaj-zgloszenie")

department = driver.find_element(By.NAME, 'department')
machine = driver.find_element(By.NAME, 'machine')
priority_level = driver.find_element(By.NAME, 'priority_level')
reporting_date = driver.find_element(By.NAME, 'date')
message = driver.find_element(By.NAME, 'message')

department.send_keys('TS')
machine.send_keys(5)
priority_level.send_keys('Niski')
# reporting_date.send_keys('2024-10-22T20:46:45')
reporting_date_click = driver.find_element(By.ID, 'today_date')
reporting_date_click.click()
message.send_keys('Zgloszenie przez formularz automatyczny')

dodaj_zgloszenie = driver.find_element(By.ID, 'przycisk_dodaj_zglosznie')
dodaj_zgloszenie.click()


time.sleep(2)

# Zamykamy przeglądarkę
driver.close()