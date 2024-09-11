from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from item import Item
import random
import time


DRIVER = None


def start_driver():
    global DRIVER

    options = Options()
    options.add_argument('--headless')

    DRIVER = webdriver.Firefox(options=options)


def end_driver():
    global DRIVER

    DRIVER.quit()
    DRIVER = None


def create_item_dict(content):
    k1 = 'a-size-medium a-color-base a-text-normal'
    k2 = 'a-size-base-plus a-color-base a-text-normal'
    p1 = 'a-price-whole'
    p2 = 'a-price-fraction'
    b = 'a-size-base a-color-secondary'
    r = 'a-icon-alt'

    item = {}
    item['title'] = content.get(k1, None)
    if not item['title']:
        item['title'] = content.get(k2, None)
    item['price'] = float(f"{content.get(p1, '0')}.{content.get(p2, '0')}".replace('..', '.').replace(',', ''))
    if not item['price']:
        item['price'] = 'N/A'
    item['link'] = content['link']
    item['past_month_buyers'] = content.get(b, '').split('+')[0].replace('K', '000')
    try:
        item['past_month_buyers'] = int(item['past_month_buyers'])
    except ValueError:
        item['past_month_buyers'] = 0

    try:
        item['rating'] = float(content[r].split('out ')[0])
    except KeyError:
        item['rating'] = 'N/A'

    return item


def get_first_link(element):
    link = element.find('a')
    if link:
        return f"https://www.amazon.com{link.get('href')}"
    return None


def extract_span_contents(element):
    spans = element.find_all('span')
    span_contents = {}

    for span in spans:
        # Get class names (can be a list, so join them into a single string)
        class_names = span.get('class', [])
        class_name_str = ' '.join(class_names) if class_names else 'no-class'

        # Get span content
        content = span.get_text(strip=True)

        # Store in dictionary
        if class_name_str not in span_contents:
            span_contents[class_name_str] = content

    return span_contents


def get_amazon_search(url):
    global DRIVER

    print(url)
    DRIVER.get(url)

    # Get the page source
    page_source = DRIVER.page_source

    while True:
        if 'Something went wrong' not in page_source:
            break

        print('Refreshing')
        time.sleep(random.uniform(2, 5))

        DRIVER.get(url)
        page_source = DRIVER.page_source

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all <div> elements with the data-asin attribute
    divs_with_asin = soup.find_all('div', attrs={'data-asin': True})

    results = []

    for div in divs_with_asin:
        asin_value = div.get('data-asin', None)
        if asin_value not in ('Unassigned', '', None):
            d = extract_span_contents(div)
            d['link'] = get_first_link(div)
            results.append(d)
        else:
            # Case 2: Divs with unassigned data-asin attribute
            # Find <li> elements within this <div>
            li_elements = div.find_all('li')
            for li_elem in li_elements:
                d = extract_span_contents(li_elem)
                d['link'] = get_first_link(li_elem)
                results.append(d)

    item_dicts = [create_item_dict(result) for result in results]
    items = [Item(item_dict) for item_dict in item_dicts]

    return items
