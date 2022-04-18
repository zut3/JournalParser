import os
from time import sleep
from pickle import load
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from datetime import date
import config
from aiocsv import AsyncWriter
import aiofiles
from random import choice


def get_data() -> list:
    sub_ids = []
    with open("site.html", "r", encoding="utf8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    sel = soup.find("select", id="subjsel")
    subject = sel.find_all("option")
    for item in subject:
        if item.get("value") != "0":
            value = item.get("value")
            sub_ids.append(value)

    with open("id.txt", "w") as file:
        [file.write(f"{e}\n") for e in sub_ids]

    return sub_ids


def get_subjects(pages: list) -> list:
    result = []
    for src in pages:
        sub = []
        soup = BeautifulSoup(src, "lxml")

        sub_data = soup.find("tr", class_="odd")

        if sub_data is not None:
            sub_datalist = sub_data.find_all("td")
            for item in sub_datalist:
                hw = item.text
                sub.append(hw)
            result.append(sub)

    return result


def get_src(ids: list, driver_path: str) -> list:
    pages = []
    url = "https://my.dnevnik76.ru/"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.add_argument("user-agent="
                         "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 "
                         "RuxitSynthetic/1.0 v5808951780353313756 t1236787695256497497")

    s = Service(executable_path=driver_path)

    driver = webdriver.Chrome(
        service=s,
        options=options)

    try:
        driver.get(url)
        sleep(0.4)
        with open("cook", "rb") as file:
            for cookie in load(file):
                driver.add_cookie(cookie)
        sleep(0.3)
        driver.refresh()
        sleep(0.3)
        for i in ids:
            driver.get(url + f"/homework/?subjsel={i}")
            sleep(0.1)
            src = driver.page_source
            pages.append(src)
        return pages
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def sort_homework(homework):
    if len(homework) <= 1:
        return homework

    pivot = choice(homework)
    pivot_num = int(pivot[0].split(" ")[0])

    right = []
    left = []
    n = homework.copy()
    n.remove(pivot)
    for e in n:
        guess = int(e[0].split(" ")[0])
        if guess > pivot_num:
            right.append(e)
        if guess <= pivot_num:
            left.append(e)

    return sort_homework(left) + [pivot] + sort_homework()


def have_file(filename: str) -> bool:
    return filename in os.listdir()


async def main() -> str:
    current_date = date.today()
    name = f"Homework_{current_date}.csv"

    if have_file(name):
        return name

    if have_file("ids.txt"):
        with open("id.txt", "r") as file:
            ids = [e.strip() for e in file.readlines()]
    else:
        ids = get_data()
    pages = get_src(ids, config.DRIVER_PATH)
    res = get_subjects(pages)

    sorted_res = sort_homework(res)

    async with aiofiles.open(name, "w", encoding="cp1251", newline="") as file:
        writer = AsyncWriter(file, delimiter=";")
        await writer.writerow(["Дата", "День недели", "Название предмета", "ДЗ", "Тема"])
        await writer.writerows(sorted_res)
    return name


if __name__ == '__main__':
    main()

