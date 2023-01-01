import time
import math

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('./chromedriver.exe')
    pytest.driver.get('https://petfriends.skillfactory.ru/login')

    time.sleep(1)

    pytest.driver.find_element_by_id('email').send_keys('xell567567567@gmail.com')
    pytest.driver.find_element_by_id('pass').send_keys('xell567567567')
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

    time.sleep(1)

    yield

    pytest.driver.quit()


def test_show_all_pets():
    images = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-img-top')))
    names = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-title')))
    descriptions = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-text')))

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_show_my_pets():
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
    pytest.driver.implicitly_wait(10)
    time.sleep(1)

    # Получаем строки со всеми питомцами
    all_pets = pytest.driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

    # Присутствуют все питомцы.
    count_pets = int(str(pytest.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]').text).split('\n')[1].split(':')[1])
    assert count_pets == len(all_pets)

    # Хотя бы у половины питомцев есть фото.
    count_photos = 0
    for one_pet in all_pets:
        photo = one_pet.find_element_by_tag_name('img').get_attribute('src')
        if photo != '': count_photos += 1
    assert count_photos >= math.ceil(count_pets/2)

    # 3 и 5 тесты
    counter_pets_par = []
    for one_pet in all_pets:
        parameters = one_pet.find_elements_by_tag_name('td')
        parameters = [str(i.text.replace(' ', '').strip()) for i in parameters]

        # У всех питомцев есть имя, возраст и порода.
        assert all(parameters)

        # В списке нет повторяющихся питомцев. (Сложное задание).
        assert parameters not in counter_pets_par
        counter_pets_par.append(parameters)

    # У всех питомцев разные имена.
    counter_pets = []
    for one_pet in all_pets:
        name = str(one_pet.find_element_by_tag_name('td').text.replace(' ', '').strip())
        assert name not in counter_pets
        counter_pets.append(name)
