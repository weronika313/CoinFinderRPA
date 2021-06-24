import random
import re

import rpa as r
import csv
from bs4 import BeautifulSoup
import requests


BASE_URL = "https://www.metalmarket.eu/"


headers_lists =(

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    r.init()
    r.url('https://www.metalmarket.eu/')
    r.click("//*[@id='ni_789']")
    r.click("//*[@id='ni_851']")


def filter_coins():
    r.click("//*[@id= 'filter_traits1_val367']")
    r.click("//*[@id= 'filter_traits510_val481']")
    r.click("//*[@id= 'filters_submit']")


    r.snap('page', 'results.png')
    r.close()

    except Exception as e:
        print(f"Error message: {e}")

