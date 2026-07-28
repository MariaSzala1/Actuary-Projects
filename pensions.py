# This project will create a fictional company pension scheme
# and will calculate how much the company's pension promises
# are worth today
import math
import random


# first let's create a function that creates one employee as a dictionary
def create_employee() -> dict:

    # generate an age between 18 and 110, assuming that employees start
    # building pension benefits from the age of 18. Use the Dutch population
    # average age of 42.8 (from cbs.nl) as the base for a Weibull
    # age distribution.
    # assume a Weibull shape parameter of 3 to create a right-skewed age
    # distribution. This is a modelling assumption, not supported by data
    # as I couldn't find any
    shape = 3
    # for a weibull distribution we know that mean = scale * gamma(1 + 1/shape)
    # and therefore after rewriting we get
    scale = 42.8 / math.gamma(1 + 1/shape)
    age = random.weibullvariate(scale, shape)

    min_age = 18
    max_age = 110

    while age < min_age or age > max_age:
        age = random.weibullvariate(scale, shape)

    age = round(age)

    # generate the annual salary in euro, that follows the lognormal 
    # distribution. I'm assuming the 40-hour full time minimum salary to be 
    # 33.674 euro (based on the information on government.nl) 
    # and the maximum pensionable salary to be 137.800 euro (based on the
    # information from belastingdienst.nl). The median salary is assumed to
    # be 48.000 euro (according to iamexpat.nl). 
    min_salary = 33674
    max_salary = 137800
    salary = random.lognormvariate(math.log(48000), 0.5)

    while salary < min_salary or salary > max_salary:
        salary = random.lognormvariate(math.log(48000), 0.5)

    salary = round(salary, 2)

    # pick a fixed retirement age (purely to keep the model more simple). 
    # Based off of the information on netherlandsworldwide.nl for 2026 
    # the retirement age is 67 
    retirement_age = 67

    # next generate the years worked by the employee. Assume the employee
    # starts working between the ages of 18 and 26. The starting age cannot
    # be larger than the employee's current age
    starting_age = random.randint(18, min(26, age))
    years_of_employment = min(age, retirement_age) - starting_age 

    # then assign the pension status value
    if age < retirement_age:
        pension_status = "active"
    else:
        pension_status = "retired"

    # now we can collect these simulated values and put them into a dictionary
    employee = {
        "age": age,
        "salary": salary,
        "years of employment": years_of_employment,
        "retirement age": retirement_age,
        "pension status": pension_status
    }

    return employee

# create another function that will take a number "n" as an input, and will 
# return a dictionary of n generated employees
def employees_sim(n: int) -> dict:
    employees = {}

    # picking the range from 1 to n+1, so that every employee has an ID
    for i in range(1, n+1):
        employees[i] = create_employee()

    return employees

# next let's create a function that will calculate the pension benefit of
# a single employee
def single_pension_calculation(employee: dict, accrual_rate: float) -> float:
    salary = employee["salary"]
    years_of_employment = employee["years of employment"]
    # For simplicity, I'm assuming that the current salary applies to
    # all previous years of employment as well
    annual_pension = salary * years_of_employment * accrual_rate
    annual_pension = round(annual_pension, 2)

    return annual_pension

# now let's define a function that will loop through all of the employees
# and will calculate the pension of each employee
def calculate_all_pensions(employees: dict, accrual_rate: float) -> dict:

    all_pensions = {}
    for employee_id, employee in employees.items():
        all_pensions[employee_id] = single_pension_calculation(employee, accrual_rate)

    return all_pensions

# next let's create a function that will estimate how much one employee's
# future annual pension payments are worth today
def one_pv_of_pension(employee: dict, accrual_rate: float, 
                             survival_prob: float, annual_survival_decrease: float, 
                             discount_rate: float) -> float:
    retirement_age = employee["retirement age"]
    age = employee["age"]
    salary = employee["salary"]
    years_of_employment = employee["years of employment"]
    years_until_retirement = max(retirement_age - age, 0)
    # I'm assuming that a person receives payments until the age of 110
    number_of_future_payments = 110 - max(age, retirement_age)
    total_pv = 0
    # I'm assuming that the first payment starts exactly when 
    # an employee reaches retirement age
    for i in range(number_of_future_payments):
        years_from_today = years_until_retirement + i
        # as we know survival rates decrease with each passing year, so we have to
        # take it into account in our simulation
        survival_for_year = max(survival_prob - annual_survival_decrease * years_from_today, 0)
        expected_payment = salary * years_of_employment * accrual_rate * survival_for_year
        present_val = expected_payment / (1 + discount_rate)**years_from_today
        total_pv += present_val

    total_pv = round(total_pv, 2)

    return total_pv

def all_pv_of_pension(employees: dict, accrual_rate: float, 
                             survival_prob: float, annual_survival_decrease: float, 
                             discount_rate: float) -> dict:
    all_pv_pensions = {} 

    for employee_id, employee in employees.items():
        all_pv_pensions[employee_id] = one_pv_of_pension(employee, accrual_rate, 
                                                         survival_prob, 
                                                         annual_survival_decrease, 
                                                         discount_rate)
    return all_pv_pensions

# now let's create a function that returns the total amount of pension
# liabilities of a company
def total_pension_liabilities(employees: dict, accrual_rate:float, 
                              survival_prob: float, annual_survival_decrease: float, 
                              discount_rate:float) -> float:
    
    all_liabilities = all_pv_of_pension(employees, accrual_rate, survival_prob,
                                  annual_survival_decrease, discount_rate)

    total = sum(all_liabilities.values())

    total = round(total, 2)

    return total



# runs the examples below only if the file is run directly
if __name__ == "__main__":
    employee = create_employee()
    employees = employees_sim(5)
    print(employee)
    print(single_pension_calculation(employee, 0.0175))
    print(calculate_all_pensions(employees, 0.0175))
    print(one_pv_of_pension(employee, 0.0175, 0.95, 0.01, 0.04))
    print(all_pv_of_pension(employees, 0.0175, 0.95, 0.01, 0.04))
    print(total_pension_liabilities(employees, 0.0175, 0.95, 0.01, 0.04))


    


    
