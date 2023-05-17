import requests
import os
from dotenv import load_dotenv
from terminaltables import SingleTable


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


def get_salary(salary_from, salary_to):
    if salary_from and salary_to:
        average_salary = int((salary_from + salary_to) / 2)
    elif salary_from and not salary_to:
        average_salary = int(salary_from * 1.2)
    else:
        average_salary = int(salary_to * 0.8)
    return average_salary


def predict_sj_rub_salary(vacancy):
    if vacancy['currency'] == 'rub':
        salary_from = vacancy['payment_from']
        salary_to = vacancy['payment_to']
        salary = get_salary(salary_from, salary_to)
        return salary


def get_sj_vacancy_statistic(vacancies):
    if vacancies[1]:
        salaries = []
        for vacancy in vacancies[1]:
            if predict_sj_rub_salary(vacancy) != 0:
                salaries.append(predict_sj_rub_salary(vacancy))
        average_salary = int(sum(salaries) / len(salaries))
        vacancy_statistic = {"vacancies_found": vacancies[0],
                             "vacancies_processed": len(salaries),
                             "average_salary": average_salary}
        return vacancy_statistic


def get_sj_languages_statistic(languages, token):
    stats = {}
    for language in languages:
        vacancies = get_total_sj_vacancies(language, token)
        stats[language] = get_sj_vacancy_statistic(vacancies)
    return stats


def create_sj_table(table_data_sj):
    table_data = [
        ['Язык программирования', 'Вакансий найдено',
         'Вакансий обработано', 'Средняя зарплата'],
    ]
    for language, stats in table_data_sj.items():
        specifics = [language, stats['vacancies_found'],
                     stats['vacancies_processed'], stats['average_salary']]
        table_data.append(specifics)
    title = 'SuperJob Moscow'
    table_instance = SingleTable(table_data, title)
    table_instance.justify_columns[0] = 'center'
    table_instance.justify_columns[1] = 'center'
    table_instance.justify_columns[2] = 'center'
    table_instance.justify_columns[3] = 'center'
    return table_instance.table


def main2():
    load_dotenv()
    token = os.getenv('SJ_TOKEN')
    languages = [
        "JavaScript", "Java", "Python", "Ruby", "PHP",
        "С++", "CSS", "C#", "C", "GO"
    ]
    table_data_sj = get_sj_languages_statistic(languages, token)
    print(create_sj_table(table_data_sj))


if __name__ == '__main__':
    main2()
