import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import sys


df=pd.read_csv('turnstile_data_master_with_weather.csv')

def entries_histogram(turnstile_weather):
    '''
    Before we perform any analysis, it might be useful to take a
    look at the data we're hoping to analyze. More specifically, lets 
    examine the hourly entries in our NYC subway data and determine what
    distribution the data follows. This data is stored in a dataframe
    called turnstile_weather under the ['ENTRIESn_hourly'] column.
    
    Why don't you plot two histograms on the same axes, showing hourly
    entries when raining vs. when not raining. Here's an example on how
    to plot histograms with pandas and matplotlib:
    turnstile_weather['column_to_graph'].hist()
    
    Your histograph may look similar to the following graph:
    http://i.imgur.com/9TrkKal.png
    
    You can read a bit about using matplotlib and pandas to plot
    histograms:
    http://pandas.pydata.org/pandas-docs/stable/visualization.html#histograms
    
    You can look at the information contained within the turnstile weather data at the link below:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    '''
   

    plt.figure()
    rainy = turnstile_weather[turnstile_weather['rain']==1]['ENTRIESn_hourly']
    clear = turnstile_weather[turnstile_weather['rain']==0]['ENTRIESn_hourly']

    plt.hist([rainy.values,clear.values], bins=25, alpha=0.85, ec='None',)
    plt.show()
    return plt



def mann_whitney_plus_means(turnstile_weather):
    '''
    This function will consume the turnstile_weather dataframe containing
    our final turnstile weather data. 
    
    You will want to take the means and run the Mann Whitney U test on the 
    ENTRIESn_hourly column in the turnstile_weather dataframe.
    
    This function should return:
        1) the mean of entries with rain
        2) the mean of entries without rain
        3) the Mann-Whitney U statistic and p-value comparing number of entries
           with rain and the number of entries without rain.  
    
    You should feel free to use scipy's Mann-Whitney implementation, and
    also might find it useful to use numpy's mean function.  
    
    Here are some documentations:
    http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    
    You can look at the final turnstile weather data at the link below:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    '''
    
    rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==1]
    no_rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==0]
    with_rain_mean = rain.mean()
    without_rain_mean = no_rain.mean()
    U, p = scipy.stats.mannwhitneyu(rain, no_rain)
    
    return with_rain_mean, without_rain_mean, U, p

def normalize_features(array):
   """
   Normalize the features in our data set.
   """
   array_normalized = (array-array.mean())/array.std()
   mu = array.mean()
   sigma = array.std()

   return array_normalized, mu, sigma

def compute_cost(features, values, theta):
    """
    Compute the cost function given a set of features / values, and the values for our thetas.
    
    This should be the same code as the compute_cost function in the lesson #3 exercises. But
    feel free to implement your own.
    """
    
    m = len(values) * 1.0
    sum_of_square_errors = np.square(np.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2*m)

    return cost

def gradient_descent(features, values, theta, alpha, num_iterations):
    """
    Perform gradient descent given a data set with an arbitrary number of features.
    
    This is the same gradient descent code as in the lesson #3 exercises. But feel free
    to implement your own.
    """
    m = len(values) * 1.0
    cost_history = []

    for i in range(num_iterations):
        # Calculate cost
        cost = compute_cost(features, values, theta)

        # Append cost to history
        cost_history.append(cost)

        # Calculate new theta
        theta = theta + alpha * (1/m) * np.dot((values - np.dot(features,theta)),features)

    return theta, pd.Series(cost_history)

def predictions(dataframe):
    '''
    The NYC turnstile data is stored in a pandas dataframe called weather_turnstile.
    Using the information stored in the dataframe, lets predict the ridership of
    the NYC subway using linear regression with gradient descent.
    
    You can look at information contained in the turnstile weather dataframe 
    at the link below:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv    
    
    Your prediction should have a R^2 value of .40 or better.
    
    Note: due to the memory and CPU limitation of our amazon EC2 instance, we will
    give you a random subet (~15%) of the data contained in turnstile_data_master_with_weather.csv
    
    If you receive a "server has encountered an error" message, that means you are hitting 
    the 30 second  limit that's placed on running your program. Try using a smaller number
    for num_iterations if that's the case.
    
    Or if you are using your own algorithm/modesl, see if you can optimize your code so it
    runs faster.
    '''

    dummy_units = pd.get_dummies(dataframe['UNIT'], prefix='unit')
    features = dataframe[['rain', 'precipi', 'Hour', 'meantempi']].join(dummy_units)
    values = dataframe[['ENTRIESn_hourly']]
    m = len(values)

    features, mu, sigma = normalize_features(features)

    features['ones'] = np.ones(m)
    features_array = np.array(features)
    values_array = np.array(values).flatten()

    #Set values for alpha, number of iterations.
    alpha = 0.1 # please feel free to play with this value
    num_iterations = 75 # please feel free to play with this value

    #Initialize theta, perform gradient descent
    theta_gradient_descent = np.zeros(len(features.columns))
    theta_gradient_descent, cost_history = gradient_descent(features_array, values_array, theta_gradient_descent,
                                                            alpha, num_iterations)

    predictions = np.dot(features_array, theta_gradient_descent)

    return predictions

def plot_residuals(turnstile_weather, predictions):
    '''
    Using the same methods that we used to plot a histogram of entries
    per hour for our data, why don't you make a histogram of the residuals
    (that is, the difference between the original hourly entry data and the predicted values).

    Based on this residual histogram, do you have any insight into how our model
    performed?  Reading a bit on this webpage might be useful:

    http://www.itl.nist.gov/div898/handbook/pri/section2/pri24.htm
    '''
    
    plt.figure()
    (turnstile_weather['ENTRIESn_hourly'] - predictions).hist()
    plt.show()
    return plt

def compute_r_squared(data, predictions):
    '''
    In exercise 5, we calculated the R^2 value for you. But why don't you try and
    and calculate the R^2 value yourself.
    
    Given a list of original data points, and also a list of predicted data points,
    write a function that will compute and return the coefficient of determination (R^2)
    for this data.  numpy.mean() and numpy.sum() might both be useful here, but
    not necessary.

    Documentation about numpy.mean() and numpy.sum() below:
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html
    '''
    numerator = np.square(data - predictions).sum()
    mean = np.mean(data)
    denominator = np.square(data - mean).sum()
    r_squared = 1 - (numerator / denominator)

    return r_squared

entries_histogram(df)
mann_whitney_plus_means(df)
   