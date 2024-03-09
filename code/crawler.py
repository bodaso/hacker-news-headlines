from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.request import urlopen
import argparse
import csv
import json
import random
import sys
import time

DATABASE_URL = "sqlite:///data/hackernews.sqlite"
HN_BASE_URL = "https://news.ycombinator.com"
# LAST_TXT_PATH = "data/last.txt"
BEST_CSV_PATH = "data/best.csv"
BEST_JSON_PATH = "data/best.json"
YT_CSV_PATH = "data/yt.csv"
YT_JSON_PATH = "data/yt.json"
DATE_FORMAT = "%Y-%m-%d"
END_DATE_FIXED = datetime.strptime("2006-10-09", DATE_FORMAT)


engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)
Base = declarative_base()


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    scores = Column(Integer)
    user = Column(String)
    date = Column(DateTime)


Base.metadata.create_all(engine)


def save_posts(posts: list[dict]) -> None:
    session = Session()
    try:
        for post in posts:
            existing_post = session.query(Post).filter_by(id=post["id"]).first()
            if existing_post:
                for key, value in post.items():
                    setattr(existing_post, key, value)
            else:
                session.add(Post(**post))
        session.commit()
    except Exception as e:
        print(f"Error saving posts: {e}")
    finally:
        session.close()


def get_single_post(item) -> dict:
    titleline = item.find("span", {"class": "titleline"})
    second = item.find_next_sibling("tr")
    id = int(item["id"])
    title = titleline.find("a").get_text()
    link = titleline.find("a")["href"]
    if link.startswith("item?id="):
        link = f"https://news.ycombinator.com/{link}"
    scores = int(
        second.find("span", {"class": "score"}).get_text().split()[0]
    )  # from "57 points" to 57
    user = second.find("a", {"class": "hnuser"})["href"].split("user?id=")[1]
    date_str = second.find("span", {"class": "age"})["title"]
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

    return {
        "id": id,
        "title": title,
        "link": link,
        "scores": scores,
        "user": user,
        "date": date,
    }


def scrape_day(day: str) -> bool:
    url = f"{HN_BASE_URL}/front?day={day}"
    try:
        with urlopen(url) as response:
            bs = BeautifulSoup(response.read(), "html.parser")
        front_posts = bs.find_all("tr", {"class": "athing"})
        # some days (e.g 2014-01-06) have 0 posts, not an error
        if front_posts:
            day_posts = [get_single_post(item) for item in front_posts]
            save_posts(day_posts)
            print(f"Saved {len(front_posts)} posts on {day} to db")
    except Exception as e:
        raise RuntimeError(f"Error on {day}: {e}")


# def save_last_date(date: str) -> None:
#     with open(LAST_TXT_PATH, "w") as file:
#         file.write(date)


def csv_to_json(csv_path, json_path):
    try:
        data = []
        with open(csv_path, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)
        json_data = json.dumps(data)  # convert to minified json
        with open(json_path, mode="w", encoding="utf-8") as json_file:
            json_file.write(json_data)
        print(f"JSON file created at {json_path}")
    except Exception as e:
        print(f"An error occurred converting csv to json: {e}")


def output_best() -> None:
    try:
        with Session() as session, open(BEST_CSV_PATH, "w", newline="") as csvfile:
            # NOTE: the query will output multiple rows for the same date if there are posts with the same max score...
            query = text(
                """
                SELECT p.*
                FROM posts p
                INNER JOIN (
                    SELECT date(date) as post_date, MAX(scores) as max_scores
                    FROM posts
                    GROUP BY date(date)
                ) as max_per_day ON p.scores = max_per_day.max_scores AND date(p.date) = max_per_day.post_date
                ORDER BY max_per_day.post_date DESC
                """
            )
            result = session.execute(query)
            column_names = result.keys()
            writer = csv.writer(csvfile)
            writer.writerow(column_names)  # Write the header row
            for row in result:
                writer.writerow(row)
        print("Saved best posts to csv file!")
    except Exception as e:
        print(f"An error occurred at the output: {e}")


# output all youtube links
def output_yt() -> None:
    try:
        with Session() as session, open(YT_CSV_PATH, "w", newline="") as csvfile:
            query = text(
                """
                SELECT p.*
                FROM posts p
                WHERE p.link LIKE '%youtube.com%'
                ORDER BY p.date DESC
                """
            )
            result = session.execute(query)
            column_names = result.keys()
            writer = csv.writer(csvfile)
            writer.writerow(column_names)  # Write the header row
            for row in result:
                writer.writerow(row)
        print("Saved youtube posts to csv file!")
    except Exception as e:
        print(f"An error occurred at the output: {e}")


def main(output: bool) -> None:
    start_date = datetime.now() - timedelta(days=1)  # start from yesterday

    if output:
        output_best()
        csv_to_json(BEST_CSV_PATH, BEST_JSON_PATH)
        output_yt()
        csv_to_json(YT_CSV_PATH, YT_JSON_PATH)
        sys.exit(0)
    else:
        days_back = 14
        for _ in range(days_back):
            current_date_str = start_date.strftime(DATE_FORMAT)
            print(f"Date: {current_date_str}")
            try:
                scrape_day(current_date_str)
            except Exception as error:
                print(error)
                # save_last_date(current_date_str)
                sys.exit(1)
            start_date -= timedelta(days=1)
            time.sleep(random.randint(1, 15))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output", help="Output top posts for each day", action="store_true"
    )
    args = parser.parse_args()
    main(args.output)
