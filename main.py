import requests

from get_salary_function import get_salary
from create_table_function import create_table
from super_job import get_sj_table


def find_hh_vacancies(language, period, page):
    base_url = "https://api.hh.ru/vacancies/"
    params = {
        'text': f'Программист {language}',
        'name': 'Москва',
        'period': f'{period}',
        'page': f'{page}'
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


def get_total_hh_vacancies(language, period):
    language_vacancies = []
    page = 0
    page_number = 1
    while page < page_number:
        vacancies = find_hh_vacancies(language, period, page)
        language_vacancies.extend(vacancies['items'])
        page_number = vacancies['pages']
        page += 1
    return len(language_vacancies), language_vacancies


def predict_hh_rub_salary(vacancy):
    salary = 0
    if not vacancy['salary']:
        return salary
    if vacancy['salary']['currency'] == "RUR":
        salary_from = vacancy['salary']['from'] or 0
        salary_to = vacancy['salary']['to'] or 0
        salary = get_salary(salary_from, salary_to)
    return salary


def get_hh_vacancy_statistic(vacancies):
    vacancies_found, language_vacancies = vacancies
    salaries = []
    for vacancy in language_vacancies:
        salary = predict_hh_rub_salary(vacancy)
        if salary:
            salaries.append(salary)
    try:
        average_salary = int(sum(salaries) / len(salaries))
        vacancy_statistic = {"vacancies_found": vacancies_found,
                             "vacancies_processed": len(salaries),
                             "average_salary": average_salary}
        return vacancy_statistic
    except ZeroDivisionError:
        return {
            "vacancies_found": vacancies_found,
            "vacancies_processed": 'ЗП не указаны',
            "average_salary": 'Не могу посчитать'
        }


def get_hh_languages_statistic(languages, period):
    stats_hh = {}
    for language in languages:
        total_vacancies = get_total_hh_vacancies(language, period)
        stats_hh[language] = get_hh_vacancy_statistic(total_vacancies)
    return stats_hh


def main():
    languages = [
        "JavaScript", "Java", "Python", "Ruby", "PHP",
        "С++", "CSS", "C#", "C", "GO"
    ]
    period = 1
    hh_languages_statistic = get_hh_languages_statistic(languages, period)
    print(create_table(hh_languages_statistic))
    get_sj_table()


if __name__ == '__main__':
    main()
