# 🚀 Async HH.ru Vacancy Scraper

[English Description](#english-version) | [Описание на русском](#russian-version)

---

<a name="english-version"></a>
## 🇬🇧 English Version

### Description
An asynchronous web scraper for **HeadHunter (hh.ru)**, Russia's leading job board. This tool allows users to search for vacancies by custom queries and regions, process data across multiple pages, and export structured results to Excel.

### ✨ Key Features
*   **Deep Search Customization:** Search by job title, company name, or keywords and filter by any region (e.g., "Russia", "Moscow").
*   **Intelligent Data Processing:**
    *   Cleans and splits raw salary strings into structured columns (`salary_from`, `salary_to`, `currency`).
    *   Identifies remote work options.
    *   Calculates experience requirements.
*   **Stealth & Safety:** Includes randomized delays and browser headers to emulate typical browser behavior.
*   **Automatic Progress Saving:** Periodically saves results to Excel during the process to prevent data loss.
*   **Modern Tech Stack:** Built with **Playwright** (Async) for fast browsing and **Pandas** for robust data manipulation.

### 🛠 Tech Stack
*   **Language:** Python 3.10+
*   **Automation:** Playwright (Chromium)
*   **Data Analysis:** Pandas, OpenPyXL
*   **Type Safety:** Python Type Hints (TypedDict, List, etc.)

---

<a name="russian-version"></a>
## 🇷🇺 Russian Version

### Описание
Асинхронный парсер для сайта **HeadHunter (hh.ru)**. Инструмент позволяет искать вакансии по произвольным запросам и регионам, обрабатывать данные с нескольких страниц и экспортировать структурированные результаты в формат Excel.

### ✨ Основные возможности
*   **Гибкий поиск:** Поиск по должности, компании или ключевым словам с выбором любого региона (Россия, города, области).
*   **Интеллектуальная обработка данных:**
    *   Автоматическая очистка и разделение зарплат на колонки (`от`, `до`, `валюта`).
    *   Определение возможности удаленной работы.
    *   Сбор информации об опыте работы и адресе.
*   **Безопасность и обход защит:** Использование случайныч задержек и заголовков для имитации типичного поведения браузера.
*   **Автоматическое сохранение прогресса:** Данные сохраняются в Excel после каждой обработанной страницы, что гарантирует сохранность информации при сбоях.
*   **Современный стек:** Использование асинхронного **Playwright** для скорости и **Pandas** для работы с таблицами.

---

## 📸 Example Output / Пример работы
![Excel Output Preview](https://github.com/felen000/hh-vacancy-parser/blob/main/result_example.png)

---

## ⚙️ Installation & Usage / Установка и запуск

1. **Clone the repository / Склонируйте репозиторий:**
   ```bash
   git clone https://github.com/felen000/hh-vacancy-parser.git
   cd hh-vacancy-parser
   ```

2. **Set up virtual environment / Настройте окружение:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # On Linux: source .venv/bin/activate
   ```

3. **Install dependencies / Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Run the scraper / Запустите парсер:**
   ```bash
   python main.py
   ```

---

## 📄 License / Лицензия
This project is for educational purposes only. Be respectful of HeadHunter's Terms of Service.
Этот проект создан исключительно в образовательных целях. Пожалуйста, соблюдайте правила пользования сайтом HeadHunter.

---
**Author / Автор:** [felen000](https://github.com/felen000)

