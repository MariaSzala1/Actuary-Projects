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
    annual_pension = salary * years_of_employment * accrual_rate
    annual_pension = round(annual_pension, 2)

    return annual_pension


# runs the examples below only if the file is run directly
if __name__ == "__main__":
    print(create_employee())
    print(single_pension_calculation({'age': 32, 'salary': 52016.6,
                                'years of employment': 12, 'retirement age': 67,
                                  'pension status': 'active'}, 0.0175))


    


    
