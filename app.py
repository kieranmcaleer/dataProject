from flask import Flask, render_template, request
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib3

app = Flask(__name__)


def getHTMLdocument(url):

    # request for HTML document of given url
    response = requests.get(url)

    # response will be provided in JSON format
    return response.text


@app.route("/", methods=["POST", "GET"])
def search():
    nyse_df = pd.read_csv("constituents_csv.csv")
    stock_list = nyse_df.values.tolist()
    stocks_with_ticker = [pair[1] + " " +
                          '(' + pair[0] + ')' for pair in stock_list]

    query = request.form.get("search")
    URL = "https://news.google.com/search?q=" + str(query) + " when%3A1d&hl"
    html_document = getHTMLdocument(URL)
    soup = BeautifulSoup(html_document, 'html.parser')
    titles = soup.find_all("a", class_="DY5T1d RZIKme")
    link_titles = [link.getText() for link in titles]
    return render_template("search.html", query=link_titles, stocks_with_ticker=stocks_with_ticker)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
