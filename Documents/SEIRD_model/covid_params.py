# Python Libraries
import statistics

# Constants (Do not change this!)
NUM_DAYS_IN_YEAR = 365

## Population Parameters
POPULATION = 1000 # Population size
DAYS_MODEL = 150 # Run the model for how many days

SOCIAL_DISTANCE_RESPONSE_FACTOR = 0.5 # The social distancing factor that represents the population's reluctance to social distancing [0,1]
POPULATION_PROPORTION_AGE_RANGE = { # Population proportion by age
  "0-14": 0.26, 
  "15-65": 0.65,
  "65+": 0.09
}

SOCIAL_DISTANCE_DAY = 57 # Day Social Distancing happened
DISEASE_SCALING_FACTOR = 0.2 # Models out how overburdened the healthcare system becomes the more infected there are. [0,1]

## Disease
r0 = 2.0 # Basic Reproductive Number of the disease (unrestrictive)
rc = 0.88 # Basic Reproductive Number of the disease when social distancing is implemented
BASE_ALPHA = 0.07 # Probability that the disease will kill a person
RHO_AGE_RANGE = { # Rate at which people die (1/6 = 6 days to kill a person)
  "0-14": 0.002,
  "15-65": 0.021,
  "65+": 0.264
}
RHO_AVERAGE = sum(POPULATION_PROPORTION_AGE_RANGE[ii]*RHO_AGE_RANGE[ii] 
  for ii in list(POPULATION_PROPORTION_AGE_RANGE.keys())) # Gets the average fatality rate across the different ages

SIGMA = 1/2.7  # The rate a person exposed to the disease becomes infectious (1/incubationPeriod)
GAMMA = 1.0 / (2.0 * (4.6 - 1.0 / SIGMA))  # The rate an infectious person recovers and moves into the recovered phase. Note that for the model it only means he does not infect anybody any more.

    © 2020 GitHub, Inc.
    Terms
    Privacy
