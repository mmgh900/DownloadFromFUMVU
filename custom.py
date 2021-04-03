import sys

from functions import *

if __name__ == '__main__':
    USER_NAME = '9812762430'
    PASSWORD = '09364661037'
    LINK = 'https://vu.um.ac.ir/course/view.php?id=1881'
    SECTION = f'section-{3}'
    PATH = './'

    current_session = login(USER_NAME, PASSWORD)
    page = find_page(LINK, SECTION, session=current_session)
    directory_name = page.find('h3').text
    download_page_content(page, f'{PATH}/{directory_name}', current_session)
