import sys
import os
import zipfile
import tarfile
import requests
from bs4 import BeautifulSoup


# Checks github.com/mozilla/geckodriver/releases for latest geckodriver release for current OS, downloads, and extracts
def get_gecko_driver():
    my_os = sys.platform
    github_url = 'https://github.com'
    gecko_url = 'https://github.com/mozilla/geckodriver/releases'

    r = requests.get(gecko_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('div', attrs={'class': 'Box Box--condensed mt-3'})
    links = results[0].find_all('a', {'class': 'd-flex flex-items-center min-width-0'})
    for link in links:
        if my_os in link['href']:
            gecko_dl_url = github_url + link['href']
            gecko = link['href'].split('/')[-1]
            print(f'Download {gecko} from: {gecko_dl_url}...')
            r = requests.get(gecko_dl_url)
            with open(gecko, 'wb') as f:
                f.write(r.content)
            print(f'Download finished')
            break

    if not gecko:
        print(f'Geckodriver for {my_os} not found. Please check {gecko_url}.')
        exit(404)

    print(f'Extracting {gecko}...')
    if gecko.endswith('zip'):
        with zipfile.ZipFile(gecko, 'r') as zip_ref:
            zip_ref.extractall()
    elif gecko.endswith('tar.gz'):
        with tarfile.open(gecko, 'r:gz') as gz_ref:
            gz_ref.extractall()
    print(f'Extraction complete')

    os.remove(gecko)

    return

if __name__ == '__main__':
    get_gecko_driver()
    print(f'Program finished. Geckodriver can be found in current directory as an .exe')
    exit(0)