from flask import Flask, render_template, request
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib3
import re
import nltk

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
    stocks_with_ticker = [pair[1] + " " + '(' + pair[0] + ')'
                          for pair in stock_list]

    query = str(request.form.get("search"))
    if query != None:
        new_query = re.findall('[^()]+', query)
    URL = "https://news.google.com/search?q=" + \
        str(new_query) + " when%3A1d&hl"
    html_document = getHTMLdocument(URL)
    soup = BeautifulSoup(html_document, 'html.parser')
    titles = soup.find_all("a", class_="DY5T1d RZIKme")
    link_titles = [link.getText() for link in titles]
    all_titles = []
    all_titles.extend(link_titles)

    return render_template("search.html", new_query=new_query, stocks_with_ticker=stocks_with_ticker, link_titles=link_titles, all_titles=all_titles)


if __name__ == "__main__":
    app.run(debug=True)
