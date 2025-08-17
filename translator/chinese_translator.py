import requests
from bs4 import BeautifulSoup
from googletrans import Translator, constants
import asyncio

async def main():
    response = requests.get('https://b.faloo.com/1490716_1.html')
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
            print(translated_text)
    else:
        print("No article content found.")

if __name__ == "__main__":
    asyncio.run(main())
