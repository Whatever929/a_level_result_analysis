import requests
import urllib.parse
from bs4 import BeautifulSoup
import pathlib
import time

STATS_URL = "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-advanced/cambridge-international-as-and-a-levels/results-statistics/"
THRESHOLD_URL = "https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-advanced/cambridge-international-as-and-a-levels/grade-threshold-tables/"
STATS_FOLDER = pathlib.Path("./statistics")
THRESHOLD_FOLDER = pathlib.Path("./threshold")

STATS_FOLDER.mkdir(parents=True, exist_ok=True)
THRESHOLD_FOLDER.mkdir(parents=True, exist_ok=True)

# Prevent overloading the website
COOLDOWN = 5

def scrape_past_stats():
    r = requests.get(STATS_URL)
    assert r.status_code == 200
    assert r.text != ""

    with open("stats.html", "w") as f:
        f.write(r.text)

    with open("stats.html", "r") as f:
        page = f.read()
        page_soup = BeautifulSoup(page, "lxml")
        target = page_soup.find_all("div", {"class": "feature"})
        current_stats = target[0]
        past_stats = target[1]

        for link in current_stats.find_all("a"):
            pdf_response = requests.get(urllib.parse.urljoin(STATS_URL, link['href']))
            assert pdf_response.status_code == 200
            assert pdf_response.content != ""
            with open(STATS_FOLDER / (link['title'] + ".pdf"), "wb") as data:
                print(f"Now writing file: {link['title']}")
                data.write(pdf_response.content)
            time.sleep(COOLDOWN)

        for link in past_stats.find_all("a"):
            pdf_response = requests.get(urllib.parse.urljoin(STATS_URL, link['href']))
            assert pdf_response.status_code == 200
            assert pdf_response.content != ""
            with open(STATS_FOLDER / (link.text + ".pdf"), "wb") as data:
                print(f"Now writing file: {link.text}")
                data.write(pdf_response.content)
            time.sleep(COOLDOWN)

def scrape_past_threshold():
    r = requests.get(THRESHOLD_URL)
    assert r.status_code == 200
    assert r.text != ""
    
    with open("threshold.html", "w") as f:
        f.write(r.text)

    with open("threshold.html", "r") as f:
        page = f.read()
        page_soup = BeautifulSoup(page, "lxml")

        def scrape_exam_series(url, folder):
            folder.mkdir(parents=True, exist_ok=True)

            r = requests.get(url)
            assert r.status_code == 200
            assert r.content != ""
            exam_soup = BeautifulSoup(r.content, "lxml")

            for subject in exam_soup.find("div", {"class":"feature"}).find_all("a"):
                subject_r = requests.get(urllib.parse.urljoin(url, subject['href']))
                assert subject_r.status_code == 200
                assert subject_r.content != ""
                with open((folder / subject['title']).with_suffix(".pdf"), "wb") as data:
                    print(f"Now writing file: {subject['title']}")
                    data.write(subject_r.content)
                time.sleep(COOLDOWN)

        for exam_series in page_soup.find_all("div", {"class": "feature"})[1].find_all("a"):
            print(f"Scraping series {exam_series['title']}")
            scrape_exam_series(urllib.parse.urljoin(STATS_URL, exam_series['href']), THRESHOLD_FOLDER / exam_series['title'])

if __name__ == "__main__":
    scrape_past_stats()
    scrape_past_threshold()
