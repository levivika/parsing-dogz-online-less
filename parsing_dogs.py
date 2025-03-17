
import requests
import json
import os
from bs4 import BeautifulSoup
URL='https://commons.wikimedia.org/wiki/List_of_dog_breeds'
def get_html(url: str):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'}
    response = requests.get(url, headers=headers)
    return response.text
def get_image(image_url: str):
    response = requests.get(image_url)
    return response.content

os.makedirs('dog_images', exist_ok=True)

def download_image(image: bytes, name_img: str):
    with open(name_img, 'wb') as file:
        file.write(image)

def get_dogs(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='wikitable')
    trs = table.find_all('tr')
    names = []
    groups = []
    local_names = []
    for tr in trs[1:]:
        tds = tr.find_all('td')
        th = tr.find('th')
        try:
            name = tds[0].text.strip()
            names.append(name)
            group = tds[1].text.strip()
            groups.append(group)
            local_name = tds[2].text.strip()
            local_names.append(local_name)

            
            img_src = th.find('span').find('img').get('src')
            if img_src:
                response=requests.get(img_src)
                if response.status_code==200:
                    image_filename=os.path.join('dog_images', f"{name}.jpg")
                    with open(image_filename, 'wb') as img_file:
                        img_file.write(response.content)
                    print('j')

        except Exception as e:
            print(f"Ошибка при обработке {name}: {e}")
            names.append('none')
            groups.append('none')
            local_names.append('none')
    print(names)
    print(groups)
    print(local_names)






html = get_html(URL)
get_dogs(html)
