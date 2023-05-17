import requests
from terminaltables import SingleTable

from main2 import main2


def find_hh_vacancies(language, period, page):
    base_url = "https://api.hh.ru/vacancies/"
    params = {
        'text': f'Программист {language}',
        'area': 1,
        'period': f'{period}',
        'page': f'{page}',
        'only_with_salary': True
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


def get_salary(salary_from, salary_to):
    if salary_from and salary_to:
        average_salary = int((salary_from + salary_to) / 2)
    elif salary_from and not salary_to:
        average_salary = int(salary_from * 1.2)
    else:
        average_salary = int(salary_to * 0.8)
    return average_salary


def predict_hh_rub_salary(vacancy):
    salary = 0
    if vacancy['salary'] and vacancy['salary']['currency'] == "RUR":
        salary_from = vacancy['salary']['from'] or 0
        salary_to = vacancy['salary']['to'] or 0
        salary = get_salary(salary_from, salary_to)
    return salary


def get_hh_vacancy_statistic(vacancies):
    if vacancies[1]:
        salaries = []
        for vacancy in vacancies[1]:
            if predict_hh_rub_salary(vacancy) != 0:
                salaries.append(predict_hh_rub_salary(vacancy))
        average_salary = int(sum(salaries) / len(salaries))
        vacancy_statistic = {"vacancies_found": vacancies[0],
                             "vacancies_processed": len(salaries),
                             "average_salary": average_salary}
        return vacancy_statistic


def get_hh_languages_statistic(languages, period):
    stats_hh = {}
    for language in languages:
        total_vacancies = get_total_hh_vacancies(language, period)
        stats_hh[language] = get_hh_vacancy_statistic(total_vacancies)
    return stats_hh


def create_hh_table(table_data_hh):
    table_data = [
        ['Язык программирования', 'Вакансий найдено',
         'Вакансий обработано', 'Средняя зарплата'],
    ]
    for language, stats in table_data_hh.items():
        specifics = [language, stats['vacancies_found'],
                     stats['vacancies_processed'], stats['average_salary']]
        table_data.append(specifics)
    title = 'HeadHunter Moscow'
    table_instance = SingleTable(table_data, title)
    table_instance.justify_columns[0] = 'center'
    table_instance.justify_columns[1] = 'center'
    table_instance.justify_columns[2] = 'center'
    table_instance.justify_columns[3] = 'center'
    return table_instance.table


def main():
    languages = [
        "JavaScript", "Java", "Python", "Ruby", "PHP",
        "С++", "CSS", "C#", "C", "GO"
    ]
    period = 1
    table_data_hh = get_hh_languages_statistic(languages, period)
    print(create_hh_table(table_data_hh))


if __name__ == '__main__':
    main()
    main2()
