def get_salary(salary_from, salary_to):
    if salary_from and salary_to:
        average_salary = int((salary_from + salary_to) / 2)
    elif salary_from and not salary_to:
        average_salary = int(salary_from * 1.2)
    else:
        average_salary = int(salary_to * 0.8)
    return average_salary
