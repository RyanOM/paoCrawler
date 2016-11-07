# -*- coding: utf-8 -*-
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from unidecode import unidecode

FRALDAS_PAGES = 3


def clean_text(text):
    """
    Removes unwanted extra spaces and \n in a given string
    """
    cleaned_text = re.sub('\s+', ' ', text).strip()
    cleaned_text = unidecode(cleaned_text).encode('ascii')
    return cleaned_text


def main():

    # Set up phantomjs as our browser
    browser = webdriver.PhantomJS(executable_path='./phantomjs/bin/phantomjs')
    print('Starting bot!\n')

    for i in range(0, FRALDAS_PAGES):
        product_list_page = 'http://www.paodeacucar.com/secoes/C4229/fraldas?&p=%s&qt=36&ftr=facetSubShelf_ss:4229_Fraldas__' % i
        browser.get(product_list_page)

        # Get page's html and find all product boxes
        page_html = browser.page_source
        soup = BeautifulSoup(page_html)
        product_list = soup.find_all("div", class_="boxProduct")

        for product in product_list:

            # Get product description
            product_name = product.find("h3", class_="showcase-item__name")
            product_name = clean_text(product_name.text)

            """
            prices = product.find_all("p", class_="singleValue")  => returns a list of all the prices in html of each product box.
            Since there are sometimes 2 prices due to promotions, we should always get the last element of this list if avaliable.
            that represents the final price.
            """
            prices = product.find_all("p", class_="singleValue")
            if len(prices):
                product_price = clean_text(prices[-1].text)
            else:
                product_price = "No price available on website."

            print(product_name)
            print(product_price)
            print("")


if __name__ == '__main__':
    main()
