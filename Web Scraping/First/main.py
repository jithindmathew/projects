import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.error


# noinspection PyTypeChecker
class Scraper:
    def __init__(self):
        self.headers_ = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
        }
        self.n = 100
        self.index = 0
        self.link_arr = np.empty(self.n, dtype='object')
        self.name_arr = np.empty(self.n, dtype='object')
        self.rating_arr = np.empty(self.n, dtype='object')
        self.num_of_rating_arr = np.empty(self.n, dtype='object')
        self.description_arr = np.empty(self.n, dtype='object')
        self.address_arr = np.empty(self.n, dtype='object')
        self.offer_price_arr = np.empty(self.n, dtype='object')
        self.original_price_arr = np.empty(self.n, dtype='object')
        self.offer_percent_arr = np.empty(self.n, dtype='object')
        self.latitude_arr = np.empty(self.n, dtype='object')
        self.longitude_arr = np.empty(self.n, dtype='object')
        self.guest_policy_arr = np.empty(self.n, dtype='object')
        self.room_type_arr = np.empty(self.n, dtype='object')

    def make_csv(self):
        df = pd.DataFrame({
            'Link': self.link_arr,
            'Name': self.name_arr,
            'Rating': self.rating_arr,
            'Number of Rating': self.num_of_rating_arr,
            'Description': self.description_arr,
            'Address': self.address_arr,
            'Offer Price': self.offer_price_arr,
            'Original Price': self.original_price_arr,
            'Offer Percent': self.offer_percent_arr,
            'Latitude': self.latitude_arr,
            'Longitude': self.longitude_arr,
            'Guest Policy': self.guest_policy_arr,
            'Room Types': self.room_type_arr
        })

        df.to_csv('result.csv', index=False, encoding='utf-8', errors='ignore')

        print('All DONE')

    def get_info(self, link):
        try:
            soup = BeautifulSoup(urlopen(Request(link, headers=self.headers_)).read(), 'html.parser')
        except urllib.error.HTTPError:
            print('INVALID LINK')
            return

        hotel_links = soup.find_all('a', class_='c-nn640c u-width100')

        for i in hotel_links:
            self.get_info_from_link(i['href'])

        self.make_csv()

    def get_info_from_link(self, hotel_id):
        soup2 = BeautifulSoup(urlopen(Request('https://www.oyorooms.com'+hotel_id, headers=self.headers_)).read(), 'html.parser')

        self.link_arr[self.index] = 'https://www.oyorooms.com' + hotel_id

        print('https://www.oyorooms.com' + hotel_id)

        name = soup2.find('h1', class_='c-1wj1luj')
        self.name_arr[self.index] = name.text if name is not None else None

        rating = soup2.find('span', class_='c-1uxth7l')
        self.rating_arr[self.index] = rating.text if rating is not None else None

        num_of_rating = soup2.find('div', class_='c-1qcdse5')
        if num_of_rating is not None:
            num_of_rating = soup2.find('div', class_='c-1qcdse5').find(text=True, recursive=False)
        self.num_of_rating_arr[self.index] = num_of_rating.text if num_of_rating is not None else None

        description = soup2.find('div', class_='c-13rpnbh')
        self.description_arr[self.index] = description.text if description is not None else None

        address = soup2.find('span', {'itemprop': 'streetAddress'})
        self.address_arr[self.index] = address.text if address is not None else None

        offer_price = soup2.find('span', class_='listingPrice__finalPrice listingPrice__finalPrice--black')
        self.offer_price_arr[self.index] = offer_price.text[1:] if offer_price is not None else None

        original_price = soup2.find('span', class_='listingPrice__slashedPrice d-body-lg')
        self.original_price_arr[self.index] = original_price.text[1:] if original_price is not None else None

        offer_percent = soup2.find('span', class_='listingPrice__percentage')
        self.offer_percent_arr[self.index] = offer_percent.text[:2] if offer_percent is not None else None

        latitude = soup2.find('meta', {'itemprop': 'latitude'})
        self.latitude_arr[self.index] = latitude['content'] if latitude is not None else None

        longitude = soup2.find('meta', {'itemprop': 'longitude'})
        self.longitude_arr[self.index] = longitude['content'] if longitude is not None else None

        guest_policy = soup2.find('ul', class_='c-f0mxva')
        self.guest_policy_arr[self.index] = guest_policy.text if guest_policy is not None else None

        room_types = soup2.find_all('span', class_='c-2j9z2q')
        room_type_list = []
        if room_types is not None:
            for i in room_types:
                room_type_list.append(i.text)

        self.room_type_arr[self.index] = room_type_list
        self.index += 1


def main():
    link = 'https://www.oyorooms.com/search?location=Mysore%20Palace%2C%20Mysore%2C%20Karnataka&latitude=12.303889&longitude=76.654444&searchType=locality&checkin=06%2F05%2F2022&checkout=09%2F05%2F2022&roomConfig%5B%5D=2&guests=2&rooms=1'
    scraper = Scraper()
    scraper.get_info(link)

    return


if __name__ == '__main__':
    main()
