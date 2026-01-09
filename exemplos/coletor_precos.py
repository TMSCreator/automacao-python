import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
produtos = soup.select(".product_pod")

with open("produtos.csv", "w", newline="", encoding="utf-8") as arquivo:
    writer = csv.writer(arquivo)
    writer.writerow(["Produto", "Preço"])

    for produto in produtos:
        nome = produto.h3.a["title"]
        preco = produto.select_one(".price_color").text
        writer.writerow([nome, preco])

print("Arquivo produtos.csv criado com sucesso!")
