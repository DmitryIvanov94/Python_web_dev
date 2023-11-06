from bs4 import BeautifulSoup
import requests


def web_page_content(url='https://ya.ru/'):
    response = requests.get(url)
    html_doc = response.text
    return BeautifulSoup(html_doc, 'html.parser')


def get_links(write_links=False):
    links_list = []
    print('Parsing available links..')
    for href in web_page_content().find_all('a'):
        link = href.get('href')
        links_list.append(link)
        if link not in ('https://ya.ru/', 'https://ya.ru', 'https://www.ya.ru'):
            for next_href in web_page_content(url=link).find_all('a'):
                next_link = next_href.get('href')
                if isinstance(next_link, str) and 'https://' in next_link:
                    links_list.append(next_link)

    if write_links is True:
        print('Writing available links..')
        with open('links.txt', 'w', encoding="utf-8") as file:
            for item in links_list:
                file.write(f"{item}\n")
    else:
        print(links_list)


if __name__ == "__main__":
    get_links(True)
