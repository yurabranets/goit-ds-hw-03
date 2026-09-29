import requests
from bs4 import BeautifulSoup
import json

authors_list=[]
quotes_list=[]
link_unique=[]




url='https://quotes.toscrape.com'


page="/"

#файл authors
while page:
    response=requests.get(url+page)
    soup=BeautifulSoup(response.text, 'lxml')
    links={a["href"] for a in soup.select("[href^='/author/']")}

    for link in links:
        if link in link_unique:
             continue
        else:
            link_unique.append(link)
            url_link='https://quotes.toscrape.com'+link
            response_link=requests.get(url_link)
            soup_link=BeautifulSoup(response_link.text, 'lxml')
            author=soup_link.find("h3", class_="author-title")
            born=soup_link.find("span", class_="author-born-date")
            location=soup_link.find("span", class_="author-born-location")
            description=soup_link.find("div", class_="author-description")

            authors_list.append({"fullname": author.text, "born_date": born.text, "born_location": location.text, "description": description.text.replace("\n", "").strip()})


    #файл quotes
    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')

    for i in range(0, len(quotes)):
        
        tags_list=[]
        tagsforquote = tags[i].find_all('a', class_='tag')
        for tagforquote in tagsforquote:
            tags_list.append(tagforquote.text)

        quotes_list.append({"tags":tags_list,"author":authors[i].text, "quotes":quotes[i].text})

    link_next=soup.find('li', class_='next')
    if link_next:
        page = link_next.find('a')["href"]
    else:
        page = None
        





with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(quotes_list, f, ensure_ascii=False, indent=4)

with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors_list, f, ensure_ascii=False, indent=4)
