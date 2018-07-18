import requests
import lxml
from lxml import html
import re
import os
import multiprocessing
from multiprocessing import Pool
import datetime



def get_books(first, last):
    name_list = []
    price_list = []
    pr_id = os.getpid()
    for i in range(first, last):
        if i%50 == 0:
            print(str(pr_id) + ' : ' + str(i))
        url = "https://www.martinus.cz/knihy/proza-poezie?nw=1&page=" + str(i)
        r = requests.get(url)
        tree = lxml.html.fromstring(r.content)
        elements = tree.xpath('//div[@class="product-item product-item--border-bottom bg-default"]')

        if len(elements) < 1:
            break
        name = elements[0].xpath('./div/div/div/div[@class="col--s-fill col--9"]/div[@class="mb-small"]/h2/a')
        price = elements[0].xpath('./div/div/div/h2[@class="text-bold mb-small"]')
        if price != [] and name != []:
            final_name = name[0].text_content()
            final_name = re.findall(r'\S+', final_name)
            final_name = " ".join(final_name)
            name_list.append(final_name)

            final_price = price[0].text
            final_price = re.findall(r'\S+', final_price)
            final_price = " ".join(final_price)
            price_list.append(final_price)
    return list(zip(name_list, price_list))

def get_books_helper(args):
    return get_books(*args)


if __name__ == '__main__':

    start_time = datetime.datetime.now()
    my_file = open('somefile.txt', 'w')

    cores = 1#multiprocessing.cpu_count()

    #getting number of pages
    url = "https://www.martinus.cz/knihy/proza-poezie"
    r = requests.get(url)
    tree = lxml.html.fromstring(r.content)
    elements = tree.xpath('//a[@class="btn btn--ghost btn--equal"][last()]')
    number_of_pages = elements[0].text_content()
    number_of_pages = re.sub(r"\s+", "", number_of_pages, flags=re.UNICODE)

    #create list of pages for processes
    quarter = (int(number_of_pages)//cores) +1
    first = 1
    last = quarter
    i = 1
    book_args = []

    while i <= cores:
        book_args.append([first, last])
        first += quarter
        last += quarter
        i += 1



    p = Pool(cores)
    final_list = p.map(get_books_helper, book_args)

    end_time = datetime.datetime.now()
    diff_time = end_time - start_time
    print(diff_time)

    for list_tmp in final_list:
        for el in list_tmp:
            my_file.write(el[0] + ", " + el[1] + "\n")

    my_file.close()

