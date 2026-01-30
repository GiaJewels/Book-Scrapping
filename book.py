import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

books_data = []

for page in range(1, 51):  # 50 pages total
    url = BASE_URL.format(page)
    response = requests.get(url)

    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]

        # Clean price properly (encoding-safe)
        price = book.find("p", class_="price_color").text
        price = price.encode("ascii", "ignore").decode()

        availability = book.find("p", class_="instock availability").text.strip()

        rating_class = book.find("p", class_="star-rating")["class"]
        rating = rating_class[1]  # One, Two, Three, Four, Five

        books_data.append({
            "product_name": title,
            "price_gbp": float(price),
            "rating": rating,
            "availability": availability,
            "review_count": None  # Not available on this site
        })

df = pd.DataFrame(books_data)
df.to_csv("books_to_scrape_data.csv", index=False)

print("Scraping complete. Data saved to books_to_scrape_data.csv")
