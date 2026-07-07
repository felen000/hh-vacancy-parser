import asyncio
import random
from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Locator,
    async_playwright,
)
from typing import TypedDict, List
import pandas as pd

user_agent: str = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
)


class Vacancy(TypedDict, total=False):
    title: str
    employer: str
    salary_from: float | None
    salary_to: float | None
    currency: str
    link: str
    address: str
    experience: str
    is_remote: bool


class Salary(TypedDict):
    salary_from: float | None
    salary_to: float | None
    currency: str


async def get_search_results_page(
    search_query: str, search_region: str, new_page: Page
) -> Page:
    baseUrlToScrap: str = "https://hh.ru"

    await new_page.goto(baseUrlToScrap, timeout=50000)
    print("Главная страница сайт открыта.")

    # find search page and fill it with search_query
    await new_page.locator("[data-qa=search-input]").fill(search_query)
    await new_page.wait_for_timeout(random.randint(500, 2000))

    # find filter btn and select region
    await new_page.locator('[data-qa="header-search-filters-button"]').click()
    region_input_locator: Locator = new_page.locator(
        '[data-qa="filter-select-area"]'
    ).locator('[data-qa="chips-trigger-input"]')
    await region_input_locator.click()

    clear_button: Locator = new_page.locator('[data-qa="search-filter-clear"]')
    await clear_button.wait_for(state="visible")
    await clear_button.click()
    await new_page.wait_for_timeout(random.randint(500, 1000))

    await region_input_locator.fill(search_region)
    await new_page.locator('[data-qa="drop"]').locator("label").first.click()
    print("Данные для поиска введены.")
    await new_page.wait_for_timeout(random.randint(500, 1000))

    # find submit button and click to go to search result page
    await new_page.locator('[data-qa="search-drawer-filters-submit"]').click()

    return new_page


async def parse_salary(salary_locator: Locator) -> Salary:
    raw_salary: str = await salary_locator.text_content() or ""
    salary: Salary = {"currency": "", "salary_from": None, "salary_to": None}

    # remove all except salary and currency
    raw_salary = raw_salary.split("за")[0].strip()

    salary["currency"] = raw_salary[-1]

    # remove currency
    raw_salary = raw_salary[:-1]

    if raw_salary.count("–") > 0:
        salary["salary_from"] = float(
            raw_salary.split("–")[0].strip().replace("\u202f", "")
        )
        salary["salary_to"] = float(
            raw_salary.split("–")[1].strip().replace("\u202f", "")
        )
    elif raw_salary.count("от") > 0:
        raw_salary = raw_salary.replace("от", "").strip()
        salary["salary_from"] = float(raw_salary.replace("\u202f", ""))
        salary["salary_to"] = None
    elif raw_salary.count("до") > 0:
        raw_salary = raw_salary.replace("до", "").strip()
        salary["salary_from"] = None
        salary["salary_to"] = float(raw_salary.replace("\u202f", ""))
    else:
        salary["salary_from"] = salary["salary_to"] = float(
            raw_salary.replace("\u202f", "")
        )
    return salary


async def parse_vacancy(vacancy_locator: Locator) -> Vacancy:
    vacancy: Vacancy = {}
    vacancy["title"] = (
        await vacancy_locator.locator(
            '[data-qa="serp-item__title-text"]'
        ).text_content()
        or ""
    )

    salary_locator: Locator = (
        vacancy_locator.locator("[class*=compensation-labels]")
        .get_by_text("за месяц")
        .or_(
            vacancy_locator.locator("[class*=compensation-labels]").get_by_text(
                "за смену"
            )
        )
    )

    if await salary_locator.count() > 0:
        salary: Salary = await parse_salary(salary_locator)
        vacancy["currency"] = salary["currency"]
        vacancy["salary_from"] = salary["salary_from"]
        vacancy["salary_to"] = salary["salary_to"]

    vacancy["employer"] = (
        await vacancy_locator.locator(
            '[data-qa="vacancy-serp__vacancy-employer-text"]'
        ).text_content()
        or ""
    )

    vacancy["address"] = (
        await vacancy_locator.locator(
            '[data-qa="vacancy-serp__vacancy-address"]'
        ).text_content()
        or ""
    )

    vacancy["link"] = (
        await vacancy_locator.locator('[data-qa="serp-item__title"]').get_attribute(
            "href"
        )
        or ""
    )

    vacancy["experience"] = (
        await vacancy_locator.locator(
            '[data-qa*="vacancy-serp__vacancy-work-experience"]'
        ).text_content()
        or ""
    )

    vacancy["is_remote"] = (
        await vacancy_locator.locator(
            '[data-qa="vacancy-label-work-schedule-remote"]'
        ).count()
        > 0
    )

    return vacancy


async def get_vacancies_from_page(page: Page) -> List[Vacancy]:
    vacancies_list: List[Vacancy] = []
    vacancies_locators_list: List[Locator] = await page.locator(
        '[data-qa="vacancy-serp__vacancy"]'
    ).all()

    for vac in vacancies_locators_list:
        vacancy: Vacancy = await parse_vacancy(vac)
        vacancies_list.append(vacancy)

    return vacancies_list


def export_to_excel(vacancies: List[Vacancy]):
    df: pd.DataFrame = pd.DataFrame(vacancies)
    if not df.empty:
        df = df.sort_values(by=["is_remote", "experience"], ascending=[False, True])
    df.to_excel("vacancies.xlsx", index=False)
    print("Данные сохранены в таблицу.")


async def get_all_vacancies(
    search_query: str, search_region: str, pages_number_to_process: int = 0
) -> List[Vacancy]:
    parsed_vacancies: List[Vacancy] = []

    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-gpu",
                "--disable-software-rasterizer",
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ],
        )
        context: BrowserContext = await browser.new_context(
            user_agent=user_agent,
            extra_http_headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Referer": "https://www.google.com/",
            },
        )
        page: Page = await context.new_page()

        print("Браузер запущен.")

        search_result_page: Page = await get_search_results_page(
            search_query, search_region, page
        )

        print("Страница с результатами поиска открыта.")

        page_counter: int = 0

        while True:
            if pages_number_to_process != 0 and page_counter >= pages_number_to_process:
                break

            await search_result_page.locator(
                '[data-qa="vacancy-serp__vacancy"]'
            ).first.wait_for()

            vacancies_from_page: List[Vacancy] = await get_vacancies_from_page(
                search_result_page
            )
            parsed_vacancies.extend(vacancies_from_page)

            next_btn_locator: Locator = search_result_page.locator(
                '[data-qa="pager-next"]'
            )

            page_counter += 1
            print(f"Страница {page_counter} обработана.")
            export_to_excel(parsed_vacancies)

            if await next_btn_locator.count() > 0:
                await next_btn_locator.click()
                await search_result_page.locator(
                    '[data-qa="vacancy-serp__vacancy"]'
                ).first.wait_for()
                await asyncio.sleep(random.uniform(0.5, 2))
            else:
                break

        await browser.close()

    return parsed_vacancies


async def main():
    try:
        pages_number_to_process: int = 0
        search_query: str = input(
            "Введите поисковый запрос(профессия, должность, или компания): "
        )
        search_region: str = input(
            "Введите регион поиска (например, Россия или Москва): "
        )

        while True:
            try:
                pages_number_to_process = int(
                    input(
                        "Введите количество страниц для парсинга или 0 для парсинга всех страниц: "
                    )
                )
                break
            except ValueError as e:
                print("Введите число!")

        print("Начинаю процесс парсинга...")
        parsed_vacancies: List[Vacancy] = await get_all_vacancies(
            search_query, search_region, pages_number_to_process
        )
        print("Процесс парсинга завершен.")

        export_to_excel(parsed_vacancies)
    except Exception as e:
        print(
            f"Произошла непредвиденная ошибка. Обратитесь за помощью к разработчику программы: {e}"
        )


asyncio.run(main())
