import sys

from functions import *

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('USER_NAME PASSWORD LINK SECTION PATH')
        exit()

    USER_NAME = sys.argv[1]
    PASSWORD = sys.argv[2]
    LINK = sys.argv[3]
    SECTION = f'section-{sys.argv[4]}'
    PATH = str(sys.argv[5])

    current_session = login(USER_NAME, PASSWORD)
    page = find_page(LINK, SECTION, session=current_session)
    directory_name = page.find('h3').text
    download_page_content(page, f'{PATH}/{directory_name}', current_session)
