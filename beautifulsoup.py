import requests
from bs4 import BeautifulSoup
import dload

url = 'https://minecraft.fandom.com/wiki/List_of_block_textures'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select('li.gallerybox')

    for block in title:
        if block.find("p").find("sup") and block.find("p").find("sup").find("span")["title"] == "This statement only applies to Bedrock Edition":
            print()
        else:
            dload.save(block.find("a")['href'], "./blocks/"+block.find(
                "p").get_text()[:-1].replace("/", "_").replace(" ", "_").replace("[JE only]", "").lower()+'.png')
    '''print(title[0].find("a")['href'])
    print(title[0].find("p").find("a")["title"])
    print(title[0].find("p").get_text())'''
    # for i in title:
    #    print(i['href'])
else:
    print(response.status_code)
