# simulates one year of insurance claims and calculates how much
# and insurer should charge as a premium
import numpy as np
import matplotlib.pyplot as plt

# First lets make a function that will simulate the annual loss

def sim_annual_loss(policyholders: int, claim_frequency: float, 
                    average_claim: float, claim_sd = float):
    # simulate the number of claims, where we assume that it is poisson distributed
    number_claims = np.random.poisson(policyholders*claim_frequency)
    # then we want to find all of the claim sizes, assuming that they
    # are normally distributed
    amount_claim = []

    for i in range(number_claims):

        claim_size = np.random.normal(average_claim, claim_sd)

        # as the normal distribution can give negative values, we want to make sure
        # to repeat the simulation, so that the claim amounts can only be positive
        while claim_size <0:
            claim_size = np.random.normal(average_claim, claim_sd)

        amount_claim.append(claim_size)
    
    # add all claim amounts to get the total loss
    total_loss = round(sum(amount_claim),2)

    return total_loss

# Then lets make a function that will run a set amount of simulations of the annual loss

def run_simulations(policyholders:int, claim_frequency:float, 
                    average_claim:float, claim_sd: float, simulations:int):
    losses = []

    # creating a loop to run the simulation a set amount of times
    for i in range(simulations):
        loss = sim_annual_loss(policyholders, claim_frequency, 
                               average_claim, claim_sd)
        
        losses.append(loss)

    return losses

# Now lets calculate the premium per policyholder. I'm going to add an extra percentage,
# called extra to make the premium a bit higher, to give some extra security to the 
# insurance company
def calculate_premium(losses:list, policyholders:int, extra: float):
    # first calculate the average annual loss
    ave_loss = np.mean(losses)
    # then calculate the loss per policyholder
    loss_per = ave_loss/policyholders
    # then we want to add that addictional percentage
    premium = round(loss_per * (1 + extra), 2)

    return premium

# Now lets make a histogram of simulated annual losses to show how their spread looks like
def hist_loss(policyholders:int, claim_frequency:float, 
                    average_claim:float, claim_sd: float, simulations:int):
    
    sim = run_simulations(policyholders, claim_frequency, average_claim,
                          claim_sd, simulations)
    
    mean = np.mean(sim)

    plt.figure()
    plt.hist(sim, bins=20)
    plt.title("Histogram of simulated annual losses")
    plt.xlabel("Loss amount")
    plt.ylabel("Number of simulations")
    plt.axvline(x=mean, color="red", linestyle="--")
    figure = plt.gcf()
    plt.show()
    return figure

# runs the examples below only if the file is run directly
if __name__ == "__main__":
    print(sim_annual_loss(100, 0.5, 300, 30))
    print(calculate_premium([12540.05, 9850.60, 11545, 12000.05, 11750], 100, 0.2))
    hist_loss(100, 0.5, 300, 30, 1000)











