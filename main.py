import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
load_dotenv("config.env")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept-Language":"en-US,en;q=0.9"
}

PRODUCT_URL = "https://www.amazon.com/CeraVe-Moisturizing-Cream-Daily-Moisturizer/dp/B00TTD9BRC/ref=sr_1_1?qid=1675303957&th=1"

response = requests.get(PRODUCT_URL, headers=HEADERS)
product_webpage = response.text

soup = BeautifulSoup(product_webpage, "html.parser")

item_price = soup.find(name="span", class_="a-offscreen")
current_price = float(item_price.getText().replace("$",""))

item_name = soup.find(name="span", class_="product-title-word-break").getText()

print(item_name, f"${current_price}")

target_price = 17 #Input here the target price you want
if current_price < target_price:
    my_email = os.getenv("MY_EMAIL") #input your email here
    my_password = os.getenv("MY_PASSWORD") #input your email password here
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.sendmail(my_email, my_email, msg=f"Subject: Amazon Price Alert!\n\n{item_name}\n is now ${current_price}\n{PRODUCT_URL}")