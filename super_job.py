import requests
import os

from get_salary_function import get_salary
from create_table_function import create_table


def get_sj_vacancies(language, token, page):
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {
        'X-Api-App-Id': token
    }
    params = {
        'catalogues': 'Разработка, программирование',
        'keyword': f'Программист {language}',
        'town': 'Москва',
        'page': page
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_total_sj_vacancies(language, token):
    language_vacancies = []
    page = 0
    while True:
        vacancies = get_sj_vacancies(language, token, page)
        language_vacancies.extend(vacancies['objects'])
        page += 1
        if not vacancies['more']:
            break
    return len(language_vacancies), language_vacancies


def predict_sj_rub_salary(vacancy):
    if vacancy['currency'] == 'rub':
        salary_from = vacancy['payment_from']
        salary_to = vacancy['payment_to']
        salary = get_salary(salary_from, salary_to)
        return salary


def get_sj_vacancy_statistic(vacancies):
    vacancies_found, language_vacancies = vacancies
    salaries = []
    for vacancy in language_vacancies:
        salary = predict_sj_rub_salary(vacancy)
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


def get_sj_languages_statistic(languages, token):
    stats = {}
    for language in languages:
        vacancies = get_total_sj_vacancies(language, token)
        stats[language] = get_sj_vacancy_statistic(vacancies)
    return stats


def get_sj_table():
    token = os.getenv('SJ_TOKEN')
    languages = [
        "JavaScript", "Java", "Python", "Ruby", "PHP",
        "С++", "CSS", "C#", "C", "GO"
    ]
    sj_languages_statistic = get_sj_languages_statistic(languages, token)
    print(create_table(sj_languages_statistic))


if __name__ == '__main__':
    get_sj_table()
