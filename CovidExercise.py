# Exercise #9. Python Programming

import numpy as np
import matplotlib.pyplot as plt

#########################################
# Question A1 - do not delete this comment
#########################################

def analyze_rating_data (filename):
    rating = np.loadtxt(filename,delimiter=',')

    # The number of seasons (number of rows in the table)
    print ('The number of seasons:')
    print (len(rating))

    # The highest rating recorded in the entire file for an episode (maximum value in the table)
    print ('The highest rating ever recorded for an episode:')
    most_popular_episode = max(rating.max(axis=0))
    print (most_popular_episode)

    # Average rating for the first episode over all seasons (average of the first column)
    print ('Average rating for the first episode over all seasons:')
    ARfFE = rating[:,0].mean()
    print (ARfFE)

    # Number of episodes which had a rating lower than 8 (how many values lower than 8 exist in the table)
    print ('Number of episodes which had a rating lower than 8:')
    ew_episodes = (rating < 8).sum()
    print (ew_episodes)

    # Is there at least one episode with a rating of 15 ? Print True or False without using IF
    print ('Is there at least one episode with a rating of 15:')
    fifteen_rating_exists = rating == 15
    print (fifteen_rating_exists.any())

    # What is the maximal total season rating ? (sum the rating in each season and print the maximum over the sums)
    print ('The maximal total season rating:')
    most_popular_season = max(rating.sum(axis=1))
    print (most_popular_season)

    #Print a vector holding the minimal rating for each episode (vector of column minimums)
    print ('Minimal rating for each episode:')
    ew_episode_for_each_season = rating.min(axis=0)
    print (ew_episode_for_each_season)

#########################################
# Question B1 - do not delete this comment
#########################################
def load_covid_world_matrix(filename, fieldname):
    f = False
    countries_lst = []
    dates_lst = []
    try:
        f = open(filename, "r")
        line = f.readline()
        field = line.split(",").index(fieldname)
        while line:
            goodline = line.split(",")
            if goodline[1] in ["", " ", "continent"]:
                line = f.readline()
                continue
            if goodline[2] not in countries_lst:
                countries_lst.append(goodline[2])
            if goodline[3] not in dates_lst:
                dates_lst.append(goodline[3])
            line = f.readline()
        countries = np.array(sorted(countries_lst))
        dates = np.array(sorted(dates_lst))
        matrix = np.zeros((len(countries), len(dates)))
        f.close()
        f = open(filename, "r")
        line = f.readline()
        while line:
            goodline = line.split(",")
            if goodline[1] in ["", " ", "continent"]:
                line = f.readline()
                continue
            if len(goodline[field]) != 0:
                 val = float(goodline[field])
                 country_index = sorted(countries_lst).index(goodline[2])
                 date_index = sorted(dates_lst).index(goodline[3])
                 matrix[country_index,date_index] = val
            line = f.readline()
        return countries, dates, matrix
    except IOError:
        print("IOError encountered")
    finally:
        if f!= False:
            f.close()

#########################################
# Question B2 - do not delete this comment
#########################################
def analyze_covid_data(countries, dates, matrix):

    print ('Are there any negative values in the table?')
    negative_val_mat = matrix < 0
    print (negative_val_mat.any())

    print ('In how many days more than 8000 new cases were identified in Israel?')
    cases_in_Israel = matrix[countries=="Israel",:]
    crazy_days_Israel = cases_in_Israel > 8000
    print(crazy_days_Israel.sum())

    print ('Number of countries with more than 1 million total cases:')
    crazy_total = matrix.sum(axis=1) > 1000000
    print (crazy_total.sum())

    print ('Name of country with the highest total number of daily cases in the first 30 days appearing in the table:')
    ind = matrix[:,0:31].sum(axis=1).argmax()
    print(countries[ind])

    print ('Date with maximal number of new cases in all countries together:')
    ind = matrix.sum(axis=0).argmax()
    print(dates[ind])

#########################################
# Question B3.1 - do not delete this comment
#########################################
def plot_country_data(matrix, countries, country):
    x = range(matrix.shape[1])
    y = matrix[countries == country, :].T
    plt.plot(x,y)
    plt.title(str(country))
    plt.xlabel("Days")
    plt.show()

#########################################
# Question B3.2 - do not delete this comment
#########################################
def plot_top_countries(matrix, countries):
    x = range(matrix.shape[1])
    srtd_indx = np.argsort(matrix.sum(axis=1))
    top_5 = matrix[srtd_indx[-5:]]
    y1 = top_5[0].T
    y2 = top_5[1].T
    y3 = top_5[2].T
    y4 = top_5[3].T
    y5 = top_5[4].T
    plt.plot(x,y1)
    plt.plot(x,y2)
    plt.plot(x,y3)
    plt.plot(x,y4)
    plt.plot(x,y5)
    plt.title("Top 5 countries")
    plt.xlabel("Days")
    plt.legend( [ str(countries[srtd_indx[-5]]), str(countries[srtd_indx[-4]]),str(countries[srtd_indx[-3]]), \
               str(countries[srtd_indx[-2]]), str(countries[srtd_indx[-1]]) ] )
    plt.show()

#########################################
# Question B3.3 - do not delete this comment
#########################################
def draw_covid_heatmap(matrix, countries):
    small_parts = matrix < 1
    matrix[small_parts] = 1
    matrix = np.log2(matrix)
    top_20_indx = np.argsort(matrix[:,0:101].sum(axis=1))[-20:]
    top_20_countries = countries[top_20_indx]
    plt.imshow(matrix[top_20_indx], cmap='afmhot', interpolation='none', aspect='auto')
    plt.yticks(np.arange(20), top_20_countries)
    plt.colorbar()
    plt.show()
