import requests
from bs4 import BeautifulSoup
from googletrans import Translator, constants
import asyncio

def scrapper():
    url = "https://b.faloo.com/1490716.html?1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content_div = soup.find('div', class_='C-Fo-Z-Mulu')
    urls = []
    for link in content_div.find_all("a", href=True):
        urls.append(link["href"])

    chapters = []
    for i in urls:
        string = "https:"+ i
        chapters.append(string)
        if string == 'https://b.faloo.com/1490716_49.html':
            break
    return chapters

async def main():
    chapters = scrapper()
    for i in chapters:
        response = requests.get(i)
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', class_='noveContent')
        if content_div:
            translator = Translator()
            from_lan = 'zh-cn'
            to_lan = 'en'
            for para in content_div.find_all('p'):
                text_to_translate = para.text.strip()
                translated = await translator.translate(text_to_translate, src=from_lan, dest=to_lan)
                translated_text = translated.text
                writetotext(translated_text)
        else:
            print("No article content found.")

def writetotext(translated_text):
    with open("translated_text.txt", "a", encoding="utf-8") as f:
        f.write(translated_text + "\n")

if __name__ == "__main__":
    asyncio.run(main())