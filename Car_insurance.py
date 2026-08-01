# In this project I will estimate an annual car insurance premium 
# of a fictional customer
import math
import random
import numpy as np

# First let's create a function that will simulate a driver
def create_driver() -> dict:
    
    # generate an age between 18 (legal age to get car insurance in the Netherlands) and
    # 85 (age when most people give up driving due to health concerns)
    # I am going to use the Beta distribution, as that way I'll be able to set the 
    # exact age limits, and make the distribution slightly right skewed
    min_age = 18
    max_age = 85
    # to get the slight right-skew
    alpha = 3
    beta = 4
    # calculating the age, first for the range of [0,1], then adjusting 
    # for our range [18, 85]
    age_proportion = random.betavariate(alpha, beta)
    age = min_age + age_proportion * (max_age - min_age)
    age = round(age)

    # next let's simulate the driving experience
    # for that we need to obtain the age when someone has received their licence.
    # I'm assuming that most people receive their licence within the ages 18 and 40,
    # where 40 is a modelling assumption, not an observed limit
    max_age_licence = min(40, age)
    alpha_l = 1 # using 1 and 4 to get a significant right skew
    beta_l = 4
    licence_age = min_age + random.betavariate(alpha_l, beta_l) * (
        max_age_licence - min_age)
    licence_age = round(licence_age)

    years_experience = age - licence_age

    # then we need the annual mileage. For that I am going to use the lognormal
    # distribution with the mean of 11.000 km as mean (based on the dutch
    # estimates on cbs.nl) and standard deviation of 5000 km (which is assumed)
    mean_mileage = 11000
    sd_mileage = 5000

    sigma_squared = math.log(1 + (sd_mileage / mean_mileage) ** 2)
    sigma = math.sqrt(sigma_squared)
    mu = math.log(mean_mileage) - sigma_squared/2

    annual_mileage = random.lognormvariate(mu, sigma)

    annual_mileage = round(annual_mileage)

    # now we need to estimate the previous accidents of a driver. The number of 
    # previous accidents will represent the ones from the past 5 years, 
    # where the driver was at fault. Lets use Poisson distribution for this count.
    # I am assuming the total of 0.5 car accidents per driver over 5 years
    # (the reason for picking 0.5 is so that the variation in having an accident is
    # higher; in reality the expected five-year accident count may be closer to 0.25)

    previous_accidents = int(np.random.poisson(0.5))

    # now let's generate the value of the car. I am going to use the lognormal
    # distribution again, as the value of a car cannot be negative. 
    # I'm assuming the mean value of a car to be 15.000 euro, and the sd to be
    # 10.000 euro. Those assumptions are made for the current value of a car, not
    # for the initial purchase value
    
    mean_car_value = 15000
    sd_car_value = 10000

    sigma_squared_c = math.log(1 + (sd_car_value / mean_car_value) ** 2)
    sigma_c = math.sqrt(sigma_squared_c)
    mu_c = math.log(mean_car_value) - sigma_squared_c/2

    car_value = random.lognormvariate(mu_c, sigma_c)

    car_value = round(car_value)

    # now let's put these values into a dictionary
    driver = {
        "age": age, 
        "years of experience": years_experience,
        "annual mileage": annual_mileage,
        "previous accidents": previous_accidents,
        "car value": car_value 
    }

    return driver

# Returns the dictionary of several policyholders
def sim_policyholders(n: int) -> dict:
    drivers = {}

    # picking from a range of 1 to n+1 so that every driver has an ID
    for i in range(1, n + 1):
        drivers[i] = create_driver()

    return drivers

# estimates one driver's expected annual claim frequency
def estimate_claim_frequency(driver: dict) -> float:

    previous_accidents = driver["previous accidents"]

    # Use 0.10 claims per year as the base frequency for a driver before applying
    # individual risk adjustments
    # (in create_driver(), the number of previous accidents is generated using a Poisson
    # mean of 0.5 accidents over five years. This corresponds to an annual frequency of
    # 0.5 / 5 = 0.10. We assume accident frequency and claim frequency are the same and
    # use 0.10 as the base before the risk adjustments)
    base_frequency = 0.10 
    frequency = base_frequency

    # Assume that each previous accident increases the base frequency by 50%
    frequency *= 1 + 0.5 * previous_accidents

    # Adjusting for mileage, because a driver travelling more than the assumed average
    # of 11,000 km per year has more exposure to accidents
    annual_mileage = driver["annual mileage"]
    average_mileage = 11000

    mileage_factor = annual_mileage/average_mileage

    frequency *= mileage_factor

    # Adjusting for driving experience, as it is reasonable to assume that an
    # inexperienced driver will be more likely to get into an accident
    experience = driver["years of experience"]

    # Assume that claim frequency decreases by 5% for every five years of driving
    # experience, with a maximum reduction of 30% (to avoid unrealistic reductions)
    five_year_blocks = min(experience//5, 6)
    frequency *= 1 - 0.05 * five_year_blocks

    return frequency

# runs the examples below only if the file is run directly 
if __name__ == "__main__":
    driver = create_driver()
    drivers = sim_policyholders(5)
    print(driver)
    print(drivers)
    print(round(estimate_claim_frequency(driver), 2))





    
    




    