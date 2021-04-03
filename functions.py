import os
from pathlib import Path
import magic
from bs4 import BeautifulSoup, SoupStrainer
import requests


def login(user_name, password):
    session = requests.Session()

    login_page = session.get('https://vu.um.ac.ir/login/index.php').content.decode('utf-8')
    login_soup = BeautifulSoup(login_page, 'html.parser')
    logintoken = login_soup.findAll('input')[1]['value']

    headers = {
        'User-Agent': 'Chrome/90.0.4430.51'}
    payload = {
        'anchor': '',
        'rememberusername': '1',
        'logintoken': logintoken,
        'username': str(user_name),
        'password': str(password)}

    session.post('https://vu.um.ac.ir/login/index.php', headers=headers, data=payload)
    return session


def find_page(link, section, session):
    main_page = session.get(link).content.decode('utf-8')
    if section != '':
        main_page = BeautifulSoup(main_page, 'html.parser')
        main_page = main_page.find('li', {'id': section})
    return main_page


def download_page_content(page, directory_path, session):
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    page.find()
    page_soup = BeautifulSoup(str(page), 'html.parser',
                              parse_only=SoupStrainer('a', href=True, attrs={'class': 'aalink'}))

    for i, link in enumerate(page_soup):
        file_name = link.find('span', {'class': 'instancename'}).text
        file_name = str(file_name).replace('فایل', '')
        file_name = f'{i + 1}- {file_name}'
        print(f"Downloading file: {file_name}...")
        resp = session.get(link['href'])
        with open('temp', 'wb') as file:
            file.write(resp.content)

        extension = magic.from_file('temp', mime=True).split('/')[-1]
        if extension == 'html':
            download_page_content(BeautifulSoup(resp.content.decode('utf-8'), 'html.parser'),
                                  f'{directory_path}/{file_name}', session)
            os.remove('temp')
        else:
            try:
                os.rename('temp', f'{directory_path}/{file_name}.{extension}')
            except FileExistsError as e:
                os.remove('temp')
                print(f"Already existed: {file_name}")
                continue
        print(f"Done: {file_name}")
