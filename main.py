import random
import re

import rpa as r
import csv
from bs4 import BeautifulSoup
import requests


BASE_URL = "https://www.metalmarket.eu/"


headers_lists =(

'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) '

'Chrome/65.0.3325.181 Safari/537.36',

'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0',

'Opera/9.80(Android2.3.4;Linux;Operamobi/adr-1107051709;U;zh-cn)Presto/2.8.149Version/11.10',

'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',

'Mozilla/5.0(Android;Linuxarmv7l;rv:5.0)Gecko/Firefox/5.0fennec/5.0',)


def enter_tab_with_coins():
    r.click("//*[@id='ni_789']")
    r.click("//*[@id='ni_851']")


def filter_coins():
    r.click("//*[@id= 'filter_traits1_val367']")
    r.click("//*[@id= 'filter_traits510_val481']")
    r.click("//*[@id= 'filters_submit']")


def get_coins():
    coins = []
    while True:
        url = r.url()
        soup = load_page(url)
        coins_soup = soup.find(id="search")
        get_all_coins_on_page(coins_soup, coins)
        if is_next_page():
            go_to_next_page()
        else:
            break

    return coins


def is_next_page():
    if r.exist('//*[@id="paging_setting_top"]/ul/li[5]/a'):
        return True
    else:
        return False


def go_to_next_page():
    r.click('//*[@id="paging_setting_top"]/ul/li[5]/a')


def get_all_coins_on_page(coins_soup, coins):
    for a_product in coins_soup.find_all("a", class_="product-name"):
        coin_url = BASE_URL + a_product["href"]

        try:
            coin = get_coin(coin_url)
            coins.append(coin)
        except AttributeError:
            pass


def get_coin(coin_url):
    coin_soup = load_page(coin_url)
    table_with_inf_about_coin = coin_soup.find("table", class_="n54117_dictionary")
    coin = collect_information_about_coin(coin_soup, table_with_inf_about_coin)
    return coin


def load_page(page_url):
    page = requests.get(page_url, headers = {'User-Agent':random.choice(headers_lists)})
    if not page:
        return None

    soup = BeautifulSoup(page.text, "html.parser")

    return soup


def collect_information_about_coin(coin_soup, table_with_inf_about_coin):
    coin = {
        "Nazwa": get_coin_name(coin_soup),
        "Cena": get_coin_price(coin_soup),
        "Średnica": get_coin_diameter(table_with_inf_about_coin),
        "Waga": get_coin_weight(table_with_inf_about_coin),
        "Stop": get_coin_alloy(table_with_inf_about_coin),
        "Nominał": get_coin_face_value(table_with_inf_about_coin),
        "Rant": get_coin_edge(table_with_inf_about_coin),
        "Producent": get_coin_producer(table_with_inf_about_coin),
    }

    return coin


def get_coin_name(coin_soup):
    try:
        coin_name = coin_soup.find("div", class_="projector_navigation")
        coin_name = coin_name.find("h1").text.strip()
        print(coin_name)
    except AttributeError:
        coin_name = "Unknown"

    return coin_name


def get_coin_price(coin_soup):
    try:
        coin_price = coin_soup.find("strong", id="projector_price_value").text.strip()

    except AttributeError:
        coin_price = "Unknown"

    return coin_price


def get_coin_diameter(table_with_inf):
    try:

        diameter_tr = table_with_inf.find(
            "span", text=re.compile("Średnica")
        ).parent.parent
        diameter = diameter_tr.find("div", class_="n54117_item_b_sub").text.strip()

    except AttributeError:
        diameter = "Unknown"

    return diameter


def get_coin_weight(table_with_inf):
    try:
        weight_tr = table_with_inf.find("span", text=re.compile("Waga")).parent.parent
        weight = weight_tr.find("div", class_="n54117_item_b_sub").text.strip()
    except AttributeError:
        weight = "Unknown"

    return weight


def get_coin_alloy(table_with_inf):
    try:

        alloy_tr = table_with_inf.find("span", text=re.compile("Stop")).parent.parent
        alloy = alloy_tr.find("div", class_="n54117_item_b_sub").text.strip()
    except AttributeError:
        alloy = "Unknown"

    return alloy


def get_coin_face_value(table_with_inf):
    try:
        face_value_tr = table_with_inf.find(
            "span", text=re.compile("Nominał")
        ).parent.parent
        face_value = face_value_tr.find("div", class_="n54117_item_b_sub").text.strip()

    except AttributeError:
        face_value = "Unknown"

    return face_value


def get_coin_edge(table_with_inf):
    try:
        coin_edge_tr = table_with_inf.find(
            "span", text=re.compile("Rant")
        ).parent.parent
        coin_edge = coin_edge_tr.find("div", class_="n54117_item_b_sub").text.strip()

    except AttributeError:
        coin_edge = "Unknown"

    return coin_edge


def get_coin_producer(table_with_inf):
    try:

        producer_tr = table_with_inf.find(
            "span", text=re.compile("Producent")
        ).parent.parent
        producer = producer_tr.find("div", class_="n54117_item_b_sub").text.strip()

    except AttributeError:
        producer = "Unknown"

    return producer


def save_coins_in_csv(coins):
    field_names = [
        "Nazwa",
        "Cena",
        "Średnica",
        "Waga",
        "Stop",
        "Nominał",
        "Rant",
        "Producent",
    ]
    with open("Coins.csv", "w", encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(coins)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":

    r.init()
    r.url(BASE_URL)

    try:
        r.init()
        r.url(BASE_URL)
        enter_tab_with_coins()
        filter_coins()
        coins = get_coins()
        save_coins_in_csv(coins)
        r.close()

    except Exception as e:
        print(f"Error message: {e}")

