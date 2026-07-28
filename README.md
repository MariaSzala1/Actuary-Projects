# Actuarial Projects
This repository contains small python projects that are based on actuarial topics. The purpose of this repository is for me to practice my coding skills, as well as to understand how probability, statistics and simulations can be used in actuarial work.

## Projects

### 1. Claims and Premiums Simulation
The purpose for this project is to show how an insurance company can use simulations to estimate future claim costs and decide how much it should charge per policyholder. 

This project simulates the total insurance claims made by a group of policyholders over the period of one year. The number of claims is generated using a Poisson distribution, while the amount of each claim is generated using a normal distribution. 
By repeating the simulation many times, we can see how much the total annual loss may differ from year to year. The results are then used to estimate the average annual loss and to calculate a premium per policyholder.

The project also creates a histogram of the simulated annual losses. This makes it easier to see how much the insurer's costs can differ between years and why premiums should account for both the expected loss and the risk of higher than average claims.

### 2. Pension Liabilities Simulation
The purpose of this project is to show how an actuary can estimate the current value of a company’s future pension promises. The project creates a fictional group of employees with different ages, salaries, years of employment and pension statuses. Employee ages are generated using a Weibull distribution, while salaries are generated using a lognormal distribution. The ranges and reference values are based mainly on Dutch data, together with several simplifying modelling assumptions.

For each employee, the project calculates the annual pension benefit based on their salary, years of employment and the chosen pension accrual rate. It then estimates how much their future pension payments are worth today by accounting for the time until retirement, survival probabilities and the discount rate. Finally, the results are combined to calculate the company’s total pension liabilities and its expected pension payments for each future year. This shows how employee characteristics, survival assumptions and discounting can affect the value and timing of a company’s pension obligations.


