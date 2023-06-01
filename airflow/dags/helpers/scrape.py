import requests
from bs4 import BeautifulSoup
import logging
import datetime
import pandas as pd


def scrape_jtiulm(output_file_name):
    # declare url target
    url = "https://jtiulm.ti.ft.ulm.ac.id/index.php/jtiulm/issue/archive"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    today = datetime.date.today()
    # get all link from the archive and stored in links as a list
    links = []
    for link in soup.find_all("a", class_="cover"):
        links.append(link.get("href"))

    paper = {
        "title": [],
        "author": [],
        "link": [],
        "date": [],
    }

    for link in links:
        page_a = requests.get(link)
        results_a = BeautifulSoup(page_a.content, "html.parser")
        for content in results_a.find_all("div", class_="obj_article_summary"):
            paper_title = content.find("div", class_="title").text.strip()
            paper_author = content.find("div", class_="authors").text
            paper_link = content.find("a").get("href")
            paper["title"].append(paper_title)
            paper["author"].append(paper_author.replace("\t", "").replace("\n", ""))
            paper["link"].append(paper_link)
            paper["date"].append(today)

    df = pd.DataFrame.from_dict(paper)
    logging.info(df.shape)
    # DataType
    df["title"] = df["title"].astype(str)
    df["author"] = df["author"].astype(str)
    df["link"] = df["link"].astype(str)
    df["date"] = df["date"].apply(pd.to_datetime)

    df.to_csv(output_file_name, index=False)


if __name__ == "__main__":
    scrape_jtiulm()
