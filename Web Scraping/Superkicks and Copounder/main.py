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
        self.n = 30
        self.index = 0
        self.item_url_arr = np.empty(self.n, dtype='object')
        self.name_arr = np.empty(self.n, dtype='object')
        self.price_arr = np.empty(self.n, dtype='object')
        self.brand_arr = np.empty(self.n, dtype='object')
        self.sizes_arr = np.empty(self.n, dtype='object')
        self.sku_arr = np.empty(self.n, dtype='object')
        self.categories_arr = np.empty(self.n, dtype='object')
        self.description_arr = np.empty(self.n, dtype='object')
        self.all_img_urls_arr = np.empty(self.n, dtype='object')

    def check_size(self):
        if self.index <= self.n - 1:
            return True

        item_url_arr_ = np.empty(2*self.n, dtype='object')
        name_arr_ = np.empty(2*self.n, dtype='object')
        price_arr_ = np.empty(2*self.n, dtype='object')
        brand_arr_ = np.empty(2*self.n, dtype='object')
        sizes_arr_ = np.empty(2*self.n, dtype='object')
        sku_arr_ = np.empty(2*self.n, dtype='object')
        categories_arr_ = np.empty(2*self.n, dtype='object')
        description_arr_ = np.empty(2*self.n, dtype='object')
        all_image_urls_arr_ = np.empty(2*self.n, dtype='object')

        item_url_arr_[:self.index] = self.item_url_arr
        name_arr_[:self.index] = self.name_arr
        price_arr_[:self.index] = self.price_arr
        brand_arr_[:self.index] = self.brand_arr
        sizes_arr_[:self.index] = self.sizes_arr
        sku_arr_[:self.index] = self.sku_arr
        categories_arr_[:self.index] = self.categories_arr
        description_arr_[:self.index] = self.description_arr
        all_image_urls_arr_[:self.index] = self.all_img_urls_arr

        self.item_url_arr = item_url_arr_
        self.name_arr = name_arr_
        self.price_arr = price_arr_
        self.brand_arr = brand_arr_
        self.sizes_arr = sizes_arr_
        self.sku_arr = sku_arr_
        self.categories_arr = categories_arr_
        self.description_arr = description_arr_
        self.all_img_urls_arr = all_image_urls_arr_
        self.n = 2*self.n

        return True

    def make_csv(self):
        df = pd.DataFrame({
            'Item URL': self.item_url_arr,
            'Name': self.name_arr,
            'Price': self.price_arr,
            'Brand': self.brand_arr,
            'Sizes': self.sizes_arr,
            'SKU': self.sku_arr,
            'Categories': self.categories_arr,
            'Description': self.description_arr,
            'All images URLs': self.all_img_urls_arr
        })

        df.to_csv('result.csv', index=False, encoding='cp1252', errors='ignore')

        print('All DONE')

    def get_info(self, link):
        try:
            soup = BeautifulSoup(urlopen(Request(link, headers={'User-Agent': 'Mozilla/5.0'})).read(), 'html.parser')
        except urllib.error.HTTPError:
            print('INVALID LINK')
            return

        req_links = set()

        for i in soup.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link'):
            req_links.add(i['href'])

        for i in req_links:
            self.get_info_from_link(i)

        next_page_link = soup.find('a', class_='next page-numbers')

        if next_page_link is not None:
            self.get_info(next_page_link['href'])
        else:
            self.make_csv()

    def get_info_from_link(self, link):
        soup = BeautifulSoup(urlopen(Request(link, headers={'User-Agent': 'Mozilla/5.0'})).read(), 'html.parser')
        if self.check_size():

            # adding the url
            self.item_url_arr[self.index] = link
            print('scraping', self.index + 1, self.item_url_arr[self.index])

            # adding the name
            name = soup.find('h1', class_='product_title entry-title')
            if name is not None:
                self.name_arr[self.index] = name.text.strip()
            else:
                self.name_arr[self.index] = 'N/A'

            # adding the price
            price = soup.find('bdi')
            if price is not None:
                if price.find(text=True, recursive=False) is not None:
                    self.price_arr[self.index] = price.find(text=True, recursive=False).replace(',', '').strip()
                else:
                    self.price_arr[self.index] = 'N/A'
            else:
                self.price_arr[self.index] = 'N/A'

            # adding the brand
            if 'copunderdog' in link:
                num = 0
                brand = soup.find('nav', class_='woocommerce-breadcrumb breadcrumb')
                if brand is not None:
                    for i in brand:
                        num += 1
                        if num == 7:
                            self.brand_arr[self.index] = i.text
                            break
                        else:
                            self.brand_arr[self.index] = 'N/A'
                else:
                    self.brand_arr[self.index] = 'N/A'

            elif 'superkicks' in link:
                brand = soup.find('p', class_='spk-brand-names')
                if brand is not None:
                    if brand.text is not None:
                        self.brand_arr[self.index] = brand.text.strip()
                    else:
                        self.brand_arr[self.index] = 'N/A'
                else:
                    self.brand_arr[self.index] = 'N/A'

            # adding the sizes
            sizes = []
            if soup.find('ul', class_='variable-items-wrapper button-variable-wrapper') is not None:
                for i in soup.find('ul', class_='variable-items-wrapper button-variable-wrapper'):
                    if i['data-value'] is not None:
                        sizes.append(i['data-value'])
                if sizes:
                    self.sizes_arr[self.index] = ', '.join(sizes)
                else:
                    self.sizes_arr[self.index] = 'N/A'
            else:
                self.sizes_arr[self.index] = 'N/A'

            # adding sku
            sku = soup.find('span', class_='sku')
            if sku is not None:
                self.sku_arr[self.index] = sku.text.strip()
            else:
                self.sku_arr[self.index] = 'N/A'

            # adding categories n
            categories = []
            if soup.find('span', class_='posted_in') is not None:
                for i in soup.find('span', class_='posted_in'):
                    if i.name == 'a':
                        categories.append(i.text)
                if categories:
                    self.categories_arr[self.index] = ', '.join(categories)
                else:
                    self.categories_arr[self.index] = 'N/A'
            else:
                self.categories_arr[self.index] = 'N/A'

            # adding Description
            description = soup.find('div', class_='woocommerce-product-details__short-description')
            if description is not None:
                if description.text is not None:
                    self.description_arr[self.index] = description.text.strip()
                else:
                    self.description_arr[self.index] = 'N/A'
            else:
                self.description_arr[self.index] = 'N/A'

            # adding image urls
            all_imag_links = set()
            if soup.find_all('div', class_='woocommerce-product-gallery__image') is not None:
                for i in soup.find_all('div', class_='woocommerce-product-gallery__image'):
                    if i.a is not None:
                        if i.a['href'] is not None:
                            all_imag_links.add(i.a['href'].strip())

                if all_imag_links:
                    self.all_img_urls_arr[self.index] = ', '.join(all_imag_links)
                else:
                    self.all_img_urls_arr[self.index] = 'N/A'
            else:
                self.all_img_urls_arr[self.index] = 'N/A'

            self.index += 1


def main():
    # https://superkicks.in/product-category/footwear/
    # https://www.copunderdog.com/product-category/sneakers/
    link = input('Paste the link : ')
    scraper = Scraper()
    scraper.get_info(link)

    return


if __name__ == '__main__':
    main()
