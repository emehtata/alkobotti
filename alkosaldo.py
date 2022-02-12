import requests
from bs4 import BeautifulSoup
import argparse

def get_availability(product_id="133287", location_id="Oulu"):
    product_url = f"https://www.alko.fi/tuotteet/{product_id}/"
    product_page = requests.get(product_url)
    soup = BeautifulSoup(product_page.content, 'html.parser')
    product_string = soup.find('title').get_text()
    print(
        f"###################### {product_string} {location_id} ######################")
    print()
    URL = f"https://www.alko.fi/INTERSHOP/web/WFS/Alko-OnlineShop-Site/fi_FI/-/EUR/ViewProduct-Include?SKU={product_id}&amp;AppendStoreList=true&amp;AjaxRequestMarker=true#"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    alko = soup.find_all(
        'li', class_='relative store-item stockInStore in-page-filter-target')
    alkos = []
    for result in alko:
        location = result.find(
            'span', class_='store-in-stock tiny-10 option-text')
        amount_left = location.findNext('span')
        if location_id in location.text:
            alkos.append(
                f'{location.text}: {amount_left.text} pulloa löytyy')
    for amount_left in alkos:
        print(amount_left)
    print()
    print("############################################################################")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hae tuotteen saldo kaupungin Alkoissa')
    parser.add_argument( '-p', '--paikkakunta', type=str, default="Oulu", required=False )
    parser.add_argument( '-t', '--tuotenro', type=str, default="133287", required=False )

    args = parser.parse_args()
    
    get_availability(product_id=args.tuotenro, location_id=args.paikkakunta)
