token="799720058:AAHbMmg0bq1MegbZ5RNtjQ9MdF9Vnvroi74"
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import random
import telebot
bot=telebot.TeleBot(token)

session=HTMLSession()

def presents(html):
    k=1
    m=1
    gifts=dict()
    while m<5:
        page={'page':m}
        resp=session.get(html, params=page)
        soup=BeautifulSoup(resp.html.html, 'html.parser')
        table=soup.find_all('div', class_="product-intro")
        for element in table:
            gifts[k]={'title': element.find('h3', class_="product-intro__title").text.replace('\n', "").strip(), \
                    "photo": element.find('div', class_="product-intro__image-box").find_next('img').get('data-src'),\
                    'price': element.find('div', class_="product-intro__price").text.replace('\n', "").replace('\t',\
                         "").replace(' ', "").strip(),\
                    "url":element.find('div', class_="product-intro__image-box").find_next('a').get('href')}
            k+=1
        m+=1
    return gifts

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    button=telebot.types.ReplyKeyboardMarkup(True)
    button.row("Стильна кухня", 'Затишний дім')
    button.row("Аксесуари", "Солодощі")
    button.row("Креативні подарунки")
    bot.send_message(message.chat.id, "Ласкаво просимо в Gift Ideas! Щоб переглядати ідеї "+\
                                      "подарунків оберіть категорію в якій бажаєте обрати"+\
                                      " подарунок!", reply_markup=button)

def send(message,url):
    num=random.randint(1,len(presents(url)))
    bot.send_photo(message.chat.id, presents(url)[num]["photo"], caption=presents(url)[num]['title']+\
        "\n"+"<b>"+presents(url)[num]['price']+"</b>"+"\n"+\
            'Можна придбати в магазині "Хочу вже"(м.Чернівці, вул.Руська, 10)'+\
            " або на сайті за посиланням: "+ presents(url)[num]['url'], parse_mode="HTML")

@bot.message_handler(content_types='text')
def button_type(message):
    if message.text=="Стильна кухня":
        url="https://hochuvzhe.ua/ua/catalog/5-stilnaya-kukhnya"
        send(message,url)
    elif message.text=='Затишний дім':
        url="https://hochuvzhe.ua/ua/catalog/4-uyutnyy-dom"
        send(message,url)
    elif message.text=='Аксесуари':
        url="https://hochuvzhe.ua/ua/catalog/7-aksessuary"
        send(message,url)
    elif message.text=='Солодощі':
        url="https://hochuvzhe.ua/ua/catalog/8-vkusnosti"
        send(message,url)
    elif message.text=='Креативні подарунки':
        url="https://hochuvzhe.ua/ua/catalog/695-originalnye-podarki"
        send(message,url)
    
        


if __name__ == "__main__":
    bot.polling()

