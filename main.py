import json
import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from db.queries import create_product
from models import ProductValid
from db.database import Base, engine

from dotenv import load_dotenv

load_dotenv()


def setup_driver(headless: bool = False) -> webdriver.Chrome:
    """Создание и настройка Selenium драйвера"""
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def extract_category(driver) -> str:
    """Извлекает путь категории товара"""
    elements = driver.find_elements(By.XPATH, '//div[@class="breadcrumbs "]/a')
    return "/".join([el.text for el in elements])


def extract_rating(driver) -> int:
    """Извлекает рейтинг товара (число)"""
    class_attr = driver.find_element(By.XPATH, '//div[@class="item__rating"]/span').get_attribute("class")
    return int(re.sub(r"\D", "", class_attr))


def extract_reviews(driver) -> int:
    """Извлекает количество отзывов"""
    reviews_text = driver.find_element(By.XPATH, '//a[@class="item__rating-link"]/span').text
    return int(re.sub(r"\D", "", reviews_text))


def extract_image_link(driver) -> str:
    image_link = driver.find_elements(By.XPATH, '//img[@class="item__slider-pic"]')[0].get_attribute("src")
    return str(image_link)


def collect_prices(driver) -> list[int]:
    """Собирает все цены со всех страниц пагинации"""
    all_prices = []

    while True:
        # собираем цены на текущей странице
        prices = driver.find_elements(By.XPATH, '//div[@class="sellers-table__price-cell-text"]')
        for p in prices:
            clean_price = int(re.sub(r"\D", "", p.text))
            all_prices.append(clean_price)

        # проверяем кнопки пагинации
        pages = driver.find_elements(By.XPATH, '//div[@class="pagination"]/li')
        next_btn = pages[-1] if pages else None

        # если нет кнопки "вперёд" или она неактивна — останавливаем цикл
        if not next_btn or "disabled" in next_btn.get_attribute("class"):
            break

        next_btn.click()
        time.sleep(1)



    return all_prices


def save_to_json(data: dict, path: str = "export/product.json"):
    """Сохраняет словарь в JSON-файл"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    with open("speed.json", "r", encoding="utf-8") as f:
        url = json.load(f)["product_url"]

    driver = setup_driver(headless=False)
    driver.get(url)
    time.sleep(1)

    # Выбираем нужный город
    driver.find_element(By.XPATH, '//a[@href="/shop/almaty/"]').click()
    time.sleep(1)

    # Извлекаем данные
    product_name = driver.find_element(By.XPATH, '//h1[@class="item__heading"]').text
    category = extract_category(driver)
    rating = extract_rating(driver)
    reviews = extract_reviews(driver)
    prices = collect_prices(driver)
    salesman_count = len(prices)
    image_link = extract_image_link(driver)

    # Формируем результат
    data = {
        "product": product_name,
        "category": category,
        "rating": rating,
        "reviews": reviews,
        "min_price": min(prices),
        "max_price": max(prices),
        "salesman_count": salesman_count,
        "image_link": image_link
    }
    product = ProductValid(**data).dict()
    create_product(product)
    save_to_json(product)
    driver.quit()
    print("[✅] Парсинг завершён. Данные сохранены в export/product.json")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Base.metadata.drop_all(bind=engine)  # Удаляет все таблицы
    # Base.metadata.create_all(bind=engine)  # Создает их заново по моделям
    main()
    print("✅ Таблицы созданы!")
