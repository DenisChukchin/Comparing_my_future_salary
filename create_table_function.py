from terminaltables import SingleTable


def create_table(languages_statistic):
    table_column_titles = [
        ['Язык программирования', 'Вакансий найдено',
         'Вакансий обработано', 'Средняя зарплата'],
    ]
    for language, stats in languages_statistic.items():
        specifics = [language, stats['vacancies_found'],
                     stats['vacancies_processed'], stats['average_salary']]
        table_column_titles.append(specifics)
    title = 'HeadHunter Moscow'
    table_instance = SingleTable(table_column_titles, title)
    table_instance.justify_columns[0] = 'center'
    table_instance.justify_columns[1] = 'center'
    table_instance.justify_columns[2] = 'center'
    table_instance.justify_columns[3] = 'center'
    return table_instance.table
