from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.request import urlopen
import csv
import json
import random
import time

NEWS_CSV_PATH = "./data/news.csv"
NEWS_JSON_PATH = "./data/news.json"
EXCEPTION_DATE_CSV_PATH = "./data/exception_date.csv"
NO_POSTS_CSV_PATH = "./data/no_posts.csv"


def get_first_line_of_csv(file_name):
    """Return the first line of csv file, or None if the file is empty"""
    try:
        with open(file_name, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            first_row = next(reader, None)
            if first_row is not None:
                return ",".join(first_row)
            return None
    except FileNotFoundError:
        print(f"File not found: {file_name}")
        return None


def get_last_line_of_csv(file_name):
    """Return the last line of csv file, or None if the file is empty"""
    try:
        with open(file_name, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            last_row = None
            for last_row in reader:
                pass
            if last_row is not None:
                return ",".join(last_row)
            return None
    except FileNotFoundError:
        print(f"File not found: {file_name}")
        return None


def is_csv_empty(file_name):
    first_line = get_first_line_of_csv(file_name)
    return first_line is None


def clear_csv_content(file_name, start_date=None):
    """
    Clear the content of the database. If a start date is provided, only clear
    the content after that date, and return the rows that were removed.
    """
    try:
        if start_date:
            # read the existing file
            with open(file_name, "r") as file:
                lines_to_keep = []
                lines_to_remove = []
                first_line = True
                for row in csv.reader(file):
                    # skip the first line (header row)
                    if first_line:
                        lines_to_keep.append(row)
                        first_line = False
                        continue
                    row_date = datetime.fromisoformat(row[0])
                    if row_date < start_date:
                        lines_to_keep.append(row)
                    else:
                        lines_to_remove.append(row)

            # write the new file
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(lines_to_keep)
            print(
                f"File {file_name} has been updated, removed entries from {start_date}"
            )
            return lines_to_remove
        else:
            # if no start date is provided, just clear the file
            with open(file_name, "w", newline="") as file:
                pass  # no need to write, just opening in 'w' mode is enough
            print(f"File {file_name} has been cleared.")
    except IOError as e:
        print(f"An IO error occurred! {e}")
    except Exception as e:
        print(f"An exception error occurred! {e}")


def append_to_csv(file_name, data):
    try:
        with open(file_name, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except IOError as e:
        print(f"CSV error: {e}")
        exit()


def get_single_post_data(post_item):
    titleline = post_item.find("span", {"class": "titleline"})
    second = post_item.find_next_sibling("tr")

    post_id = post_item["id"]
    title = titleline.find("a").get_text()
    link = titleline.find("a")["href"]
    upvotes = int(
        second.find("span", {"class": "score"}).get_text().split()[0]
    )  # from "57 points" to "57"
    date = second.find("span", {"class": "age"})[
        "title"
    ]  # example: 2024-01-19T17:42:05

    if link.startswith("item?id="):
        link = f"https://news.ycombinator.com/{link}"

    return {
        "id": post_id,
        "title": title,
        "link": link,
        "upvotes": upvotes,
        "date": date,
    }


def get_front_posts(date):
    """
    The /front?day=yyyy-mm-dd page does not order posts in order and posts could
    be from a day or two ago, so we have to store several days and check the date.
    """
    formatted_date = date.strftime("%Y-%m-%d")
    url = f"https://news.ycombinator.com/front?day={formatted_date}"
    try:
        html = urlopen(url)
        bs = BeautifulSoup(html.read(), "html.parser")
        total_posts = []
        front_posts = bs.find_all("tr", {"class": "athing"})
        if len(front_posts) > 0:
            for post in front_posts:
                total_posts.append(get_single_post_data(post))
            print(f"Found front posts for {formatted_date}")
            return total_posts
        else:
            print(f"No front posts found for {formatted_date}")
            with open(NO_POSTS_CSV_PATH, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([f"{formatted_date}"])
    except Exception as e:
        print(f"{formatted_date}: {e}")
        # we'll store the last exception date
        with open(EXCEPTION_DATE_CSV_PATH, mode="w") as file:
            writer = csv.writer(file)
            writer.writerow([f"{formatted_date}"])
        exit()


def csv_to_json(csv_path, json_path):
    data = []
    with open(csv_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    # convert to minified json
    json_data = json.dumps(data)
    with open(json_path, mode="w", encoding="utf-8") as json_file:
        json_file.write(json_data)
    print(f"JSON file created at {json_path}")


def get_start_date(mode):
    if mode == "beginning":
        # find the last date in the csv file
        if not is_csv_empty(NEWS_CSV_PATH):
            start_date = datetime.strptime(
                get_last_line_of_csv(NEWS_CSV_PATH).split(",")[0], "%Y-%m-%dT%H:%M:%S"
            )
        else:
            # if the csv file is empty, start from the beginning
            start_date = datetime(2006, 10, 9)
    else:
        # "normal" mode: HN upvotes stops at 2 weeks
        two_weeks_ago = datetime.today() - timedelta(weeks=2)
        start_date = two_weeks_ago.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_date


if __name__ == "__main__":
    if not is_csv_empty(EXCEPTION_DATE_CSV_PATH):
        start_date = datetime.strptime(
            get_first_line_of_csv(EXCEPTION_DATE_CSV_PATH), "%Y-%m-%d"
        )
    else:
        start_date = get_start_date("normal")

    print(f"start_date: {start_date}")

    end_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    print(f"end_date: {end_date}")

    # start the program, first clear from start date
    old_news = clear_csv_content(NEWS_CSV_PATH, start_date)

    # also clear the exception date csv file
    clear_csv_content(EXCEPTION_DATE_CSV_PATH)

    current_date = start_date

    # TODO: what if the date range is too big? this list could get huge
    all_posts = []
    while current_date <= end_date:
        posts = get_front_posts(current_date)
        if posts:
            all_posts.extend(posts)
        current_date += timedelta(days=1)
        time.sleep(random.randint(1, 15))


    # filter all posts, remove duplicated posts by id
    unique_posts = []
    unique_ids = set()
    for post in all_posts:
        if post["id"] not in unique_ids:
            unique_posts.append(post)
            unique_ids.add(post["id"])


    current_date = start_date
    while current_date <= end_date:
        # find posts for the current date
        posts = [post for post in unique_posts if post["date"].split("T")[0] == current_date.strftime("%Y-%m-%d")]
        if len(posts) > 0:
            posts.sort(key=lambda x: x["upvotes"], reverse=True)
            # find post with same date from old news
            old_news_post = [post for post in old_news if post[0].split("T")[0] == current_date.strftime("%Y-%m-%d")]
            old_news_score = int(old_news_post[0][1]) if old_news_post else 0
            if old_news_post and posts[0]["upvotes"] > old_news_score:
                print(f"Found a new top post for {current_date}")
                append_to_csv(NEWS_CSV_PATH, [[posts[0]["date"], posts[0]["upvotes"], posts[0]["id"], posts[0]["title"], posts[0]["link"]]])
            else:
                print(f"Keeping same news for {current_date}")
                append_to_csv(NEWS_CSV_PATH, [[old_news_post[0][0], old_news_post[0][1], old_news_post[0][2], old_news_post[0][3], old_news_post[0][4]]])   
        else:
            print(f"No posts found for {current_date}")
            with open(NO_POSTS_CSV_PATH, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([f"{current_date}"])
        current_date += timedelta(days=1)

    # export a json copy
    csv_to_json(NEWS_CSV_PATH, NEWS_JSON_PATH)

    print("Program complete!")
