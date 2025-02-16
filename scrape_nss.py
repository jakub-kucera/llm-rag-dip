import os
import urllib

import requests
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0"


def scrape_ness(start_year: int, end_year: int, output_dir: str):
    usneseni_links = []
    for year in range(start_year, end_year+1):
        print(f"Year: {year}")
        year_view = requests.get(f'https://sbirka.nssoud.cz/cz/{year}', headers={'User-Agent': USER_AGENT})
        soup = BeautifulSoup(year_view.text, 'html.parser')
        links_boxes = soup.find_all('div', {'class': 'list-item'})
        sublinks = [urllib.parse.urljoin('https://sbirka.nssoud.cz/', box.find('a').get('href')) for box in links_boxes]
        print(f"Number of sublinks: {len(sublinks)}")
        for sublink in sublinks:
            r = requests.get(sublink, headers={'User-Agent': USER_AGENT})
            soup = BeautifulSoup(r.text, 'html.parser')
            for box in soup.find_all('div', {'class': 'list-item'}):
                usneseni_links.append(urllib.parse.urljoin('https://sbirka.nssoud.cz/', box.find('a').get('href')))

    print(f"Number of usneseni_links: {len(usneseni_links)}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for c, link_usneseni in enumerate(usneseni_links):
        print(f"#{c} link: {link_usneseni}")
        r = requests.get(urllib.parse.urljoin('https://sbirka.nssoud.cz/', link_usneseni), headers={'User-Agent': USER_AGENT})
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.find('h2').text
        text = soup.find('div', {'class': 'jud'}).text
        num_tag = soup.find('div', {'class': 'num-tag-wrap'}).text.strip().replace('/', '_')

        with open(f'{output_dir}/{num_tag}.txt', 'w') as f:
            f.write(text)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_year", "-s", type=int)
    parser.add_argument("--end_year", "-e", type=int)
    parser.add_argument("--output_dir", "-o", type=str)
    args = parser.parse_args()
    scrape_ness(args.start_year, args.end_year, args.output_dir)