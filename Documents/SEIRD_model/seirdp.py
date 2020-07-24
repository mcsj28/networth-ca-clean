## Libraries
# Python Libraries
import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt
import math

# Local Libraries
import covid_params # Change the values here if you want to adjust one variable at a time

## SEIRD model
# To generate a model, declare an instance of the object, call its method solve() and you will get X, S, E, I, R, D arrays
# These arrays correspond to Number of days, susceptible, exposed, infectious, recovered and dead respectively
# @param {float}: r0 - Basic Reproductive Number of the disease (unrestrictive)
# @param {float}: rc - Basic Reproductive Number of the disease when social distancing is implemented
# @param {float}: gamma - The rate an infected person recovers from the disease (1/infectiousPeriod)
# @param {float}: sigma - The rate a person exposed to the disease becomes infectious (1/incubationPeriod)
# @param {float}: baseAlpha - Probability that disease kills a person
# @param {float}: rho - Probability that people will die from the disease
# @param {float}: socDistResponseFactor - Models out how responsive the population is to social distancing. [0,1]
# @param {float}: diseaseScalingFactor - Models out how overburdened the healthcare system becomes the more infected there are. [0,1]
# @param {bool}: debugFlag - Debugging purposes
class seird():
  def __init__(self, r0, rc, gamma, sigma, baseAlpha, rho, socDistResponseFactor=1.0, diseaseScalingFactor=0.1, debugFlag=False):
    # Assign variables
    self.r0 = r0
    self.rc = rc
    self.gamma = gamma
    self.sigma = sigma
    self.baseAlpha = baseAlpha
    self.rho = rho
    self.socDistResponseFactor = socDistResponseFactor
    self.diseaseScalingFactor = diseaseScalingFactor

    # Flags
    self.debugFlag = debugFlag
    self.thresholdPrintFlag = False # When True, prints a statement of when countermeasures go into effect

  ## The main heart of the model
  # @param {array of arrays}: Y - Arrays containg arrays of the previous steps' population at each stage
  # @param {integer}: x - Number of days since day 0
  # @param {integer}: N - Total Population
  # @param {float}: r0 - Basic Reproductive Number of the disease (unrestrictive)
  # @param {integer}: thrDay - Day that social distancing was implemented
  # @param {float}: rc - Basic Reproductive Number of the disease when social distancing is implemented
  # @param {float}: gamma - The rate an infected person recovers from the disease (1/infectiousPeriod)
  # @param {float}: sigma - The rate a person exposed to the disease becomes infective (1/incubationPeriod)
  # @param {float}: rho - Fatality rate of the disease per day
  def model(self, Y, x, N, r0, thrDay, rc, gamma, sigma, rho):
    S, E, I, R, D = Y

    # Disease population hits threshold. Begin social distancing
    # if ((I + R + D) > thrPop and x < thrDay):
    #   thrDay = x

    # Obtaining beta from beta = Rc * gamma. Use Rc during and after social distancing has been implemented.
    if (x >= thrDay):
        if self.thresholdPrintFlag and self.debugFlag:
          print("Countermeasures come into effect on day: " + str(round(x)))
          self.thresholdPrintFlag = False

        # beta = alpha*gamma
        beta = self.logisticFunction(x, thrDay, self.socDistResponseFactor) * gamma
    else:
     # Use R0 during and after social distancing has been implemented.
      beta = r0*gamma

     # Obtaining alpha
    alpha = self.alphaGenerated(I, N)

    # Main ordinary differential equations to calculate population per day
    dS = - beta * S * I / N
    dE = beta * S * I / N - sigma * E
    dI = sigma * E - (1 - alpha) * gamma * I - alpha * rho * I
    dR = (1 - alpha)*gamma * I
    dD = alpha*rho*I

    return dS, dE, dI, dR, dD

  ## Modelling the gradual trend to Rc
  # @param {integer}: x - The current day
  # @param {integer}: x0 - The day that social distancing happens
  # @param {float}: k - The social distancing factor that represents the population's reluctance to social distancing [0,1]
  def logisticFunction(self, x, x0, k):
    return (self.r0 - self.rc)/(1 + math.exp(-k*(-x + x0))) + self.rc

  ## Models out how more potent the disease is at killing people the more overburdened the healthcare system is
  # @param {integer}: I - Population number that are infectious
  # @param {integer}: N - Total population number
  def alphaGenerated(self, I, N):
    overworkedAlpha = self.diseaseScalingFactor * I / N # If the healthcare is not able to cope, this comes into play
    return overworkedAlpha + self.baseAlpha

  ## Modelling out the population numbers, based on object variables and method params
  # @param {integer}: population - Total population number
  # @param {integer}: N - Total population number
  # @param {integer}: thrDay - Day social distancing takes into effect
  # @param {integer}: daysModel - Number of days to model out pandemic
  def solve(self, population, E0, thrDay, daysModel):
    X = np.arange(daysModel)  # time steps array
    N0 = population - E0, E0, 0, 0, 0  # S, E, I, R at initial step
    self.thresholdPrintFlag = True
    
    y_data_var = scipy.integrate.odeint(self.model, N0, X, args=(
      population, self.r0, thrDay, self.rc, self.gamma, self.sigma, self.rho))
      
    S, E, I, R, D = y_data_var.T  # transpose and unpack
    return X, S, E, I, R, D  # note these are all arrays

## If this is the main python file...
if __name__ == "__main__":
  E0 = 1  # exposed at initial time step
  N = covid_params.POPULATION
  debugFlag = True

  modelInstance = seird(covid_params.r0, covid_params.rc, covid_params.GAMMA, covid_params.SIGMA,
    covid_params.BASE_ALPHA, covid_params.RHO_AVERAGE, covid_params.SOCIAL_DISTANCE_RESPONSE_FACTOR, covid_params.DISEASE_SCALING_FACTOR, debugFlag)
  X, S, E, I, R, D = modelInstance.solve(N, E0, covid_params.SOCIAL_DISTANCE_DAY, covid_params.DAYS_MODEL)

  # Plot percentages of Population
  fig = plt.figure(dpi=75, figsize=(20,16))
  ax = fig.add_subplot(111)
  ax.plot(X, S/N*100, 'o', color='green', label='Susceptible')
  ax.plot(X, E/N*100, 'o', color='yellow', label='Exposed (realtime)')
  ax.plot(X, I/N*100, 'o', color='red', label='Infected (realtime)')
  ax.plot(X, R/N*100, 'o', color='blue', label='Recovered')
  ax.plot(X, D/N*100, '-', color='grey', label='Dead (Disease)')

  # Plot threshold day
  plt.axvline(x=covid_params.SOCIAL_DISTANCE_DAY, color='black')

  # Prepare plot for viewing
  ax.set_xlabel('Time (days)')
  ax.set_ylabel('% Of Population' + str(N))
  ax.set_ylim(bottom=0.0, top=100.0)
  legend = ax.legend(title='SEIRD model')

  # Print numbers
  print('Number of Susceptible at Day ' + str(covid_params.DAYS_MODEL) + ': ' + str(round(S[-1])))
  print('Number of Exposed at Day ' + str(covid_params.DAYS_MODEL) + ': ' + str(round(E[-1])))
  print('Number of Infected at Day ' + str(covid_params.DAYS_MODEL) + ': ' + str(round(I[-1])))
  print('Number of Recovered at Day ' + str(covid_params.DAYS_MODEL) + ': ' + str(round(R[-1])))
  print('Number of Dead at Day ' + str(covid_params.DAYS_MODEL) + ': ' + str(round(D[-1])))
  print("Total Number of Population: " + str(round(N)))

  # Display plot
  plt.show()