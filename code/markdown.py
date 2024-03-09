import csv
from datetime import datetime
from crawler import BEST_CSV_PATH

README_PATH = "./README.md"
START_PLACEHOLDER = "NEWS PREVIEW BEGIN"
END_PLACEHOLDER = "NEWS PREVIEW END"


def read_csv(file_path):
    with open(file_path, "r") as file:
        lines = []
        for row in csv.reader(file):
            lines.append(row)
    return lines


if __name__ == "__main__":
    # read the news csv, extract the top 365 items
    news = read_csv(BEST_CSV_PATH)[1:366]

    # iterate through the news and produce markdown content
    markdown_content = f"<!-- {START_PLACEHOLDER} -->\n"
    markdown_content += "| :coffee: | Title | 💬 |\n"
    markdown_content += "| --- | --- | --- |\n"

    for row in news:
        id, title, link, scores, user, date = row
        # change the date format from sqlite datetime to DD-MM-YYYY
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        date = date_obj.strftime("%d-%m-%Y")
        markdown_content += f"| {scores} | [{title}]({link}) | [{date}](https://news.ycombinator.com/item?id={id}) |\n"
    markdown_content += f"<!-- {END_PLACEHOLDER} -->\n"

    # read the readme file and replace the content between the placeholders
    with open(README_PATH, "r") as file:
        readme = file.readlines()

    start_index = next(i for i, line in enumerate(readme) if START_PLACEHOLDER in line)
    end_index = next(i for i, line in enumerate(readme) if END_PLACEHOLDER in line)

    readme[start_index : end_index + 1] = [markdown_content]

    with open(README_PATH, "w") as file:
        file.writelines(readme)

    print("README.md updated successfully!")
