import requests
import lxml
from lxml import html
import re

i = 2315
name_list = []
price_list = []
name_price_list = []
my_file= open('somefile.txt', 'w')


while True:
    url = "https://www.martinus.cz/knihy/proza-poezie?nw=1&page=" + str(i)
    r = requests.get(url)
    tree = lxml.html.fromstring(r.content)
    elements = tree.xpath('//div[@class="product-item product-item--border-bottom bg-default"]')

    if len(elements) < 1:
        break
    for el in elements:
        name = el.xpath('./div/div/div/div[@class="col--s-fill col--9"]/div[@class="mb-small"]/h2/a')
        price = el.xpath('./div/div/div/h2[@class="text-bold mb-small"]')
        if price != [] and name != []:
            for el_n in name:
                final_name = el_n.text_content()
                final_name = re.findall(r'\S+', final_name)
                final_name = " ".join(final_name)
                name_list.append(final_name)
                print(final_name)
                my_file.write(final_name + ' ')
            for el_p in price:
                final_price = el_p.text
                final_price = re.findall(r'\S+', final_price)
                final_price = " ".join(final_price)
                price_list.append(final_price)
                my_file.write(final_price + '\n')
    name_price_list = tuple(zip(name_list, price_list))
    i += 1

my_file.close()

