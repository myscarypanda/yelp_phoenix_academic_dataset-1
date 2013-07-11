# Cross Validation for the recommendation algorithm
# Calculate rms error between predicted and actual ratings.

"""
Created on Mon Jun 17 10:18:43 2013

@author: lisaqian
"""

from Recommend import *
import numpy as np
from math import sqrt
from CrossValidation_set import *
import matplotlib.pyplot as plt
from CalcSimilarities import *


#Using BReviews_HO, BusinessLookup, calculate the similarities of each pair of businesses
#######################
#
#matches = {} #top matches for each business
#
#
#for business in BusinessReviewsHO:
    #scores = getTopMatches(BusinessReviewsHO, business, n=50)
    #matches[business] = scores

#============================================================================#    
#This function calculates the predicted rating User will give a Business
#INPUT: user_id, business_id
#OUTPUT: (double predictedRating) 
def predictRating(user_id, business_id, BReviews):
    
    mu = 3.794 #avg rating for all businesses (global baseline)
    
    userBaseline = UserLookup[user_id][2] - mu #user baseline
    businessBaseline = BusinessLookup[business_id][2] - mu #business baseline
    
    userRatings = UserReviews[user_id] #these are all the ratings that user has reviewed
    #scores = {} #dictionary of predicted ratings and corresponding business 
    score = 0    
    totalSim = 0
    
    
    #iterate over items rated by the user; calculate similarity
    for (b, rating) in userRatings.items():
        
        #business baseline (for businesses rated by user)
        bBase = BusinessLookup[b][2] - mu

        #calculate similarty between business and b
        sim = calcSim(BReviews, business_id, b)
        
        #now calculate predicted rating as weighted sum of similarity and rating
        score += 1.0*sim*(rating - (mu+ userBaseline+bBase))
        #score += 1.0*sim*(rating)
        
        #sum of all the similarities
        totalSim +=sim
        
     #find average predicted ratings
    if totalSim == 0:
        #user has not visited any businesses that are similar to the one in question.
        #return the baseline
        predictedRating = (mu+businessBaseline+userBaseline)

    else:
        predictedRating = (mu+userBaseline+businessBaseline)+1.0*score/totalSim
        #predictedRating = (mu+businessBaseline+userBaseline)       
        
    if predictedRating > 5:
        predictedRating = 5
    elif predictedRating < 1:
        predictedRating = 1

    return round(2.0*predictedRating)/2
    
    
####################
###MAIN FUNCTION####
####################
#For the HoldOut set, estimate rating with function above. 
#Compare to actual value and compute the rms error
#Plot the distribution of error (estimated - actual)
deviations = []
ratings = []
predictions = []
sumOfSquares = 0
sumOfSquaresBA = 0
avgDeviations = []

#FOLLOWING DATA STRUCTURES FROM CrossValidation_set
#BReviews_HO: BusinessReviews minus the items from the holdout set
#HoldOut: {(user, business): Actual Rating}

#for each review in hold out, calculate predicted rating
for key in HoldOut.keys():
    user = key[0]
    business = key[1]
    pred = predictRating(user, business, BReviews_HO)
    businessAvg = BusinessLookup[business][2]
    error = pred - HoldOut[key]
    deviations.append(error)
    avgDeviations.append(businessAvg - HoldOut[key]) #deviation if prediction is bus average
    sumOfSquares += pow(error,2)
    sumOfSquaresBA += pow(businessAvg - HoldOut[key], 2)
    ratings.append(HoldOut[key])
    predictions.append(pred)
    
#rms error for CF
rms = sqrt(sumOfSquares/len(HoldOut))
print rms

#rms error for BA
rms_BA = sqrt(sumOfSquaresBA/len(HoldOut))
print rms_BA

#################################
##PLOT HISTOGRAMS OF PREDICTION ERRORS###
params = {'legend.fontsize': 24,
          'font.size' : 30,
          'axes.linewidth': 0.5,
          'legend.linewidth': 0.5}
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.rcParams.update(params)
plt.figure(figsize=(30, 10)) 
bins = np.linspace(-4, 4, 18)

plt.subplot(121)
plt.hist(avgDeviations, bins, alpha=.9, rwidth=0.6, color='crimson')
plt.title('Prediction = Business Average')
plt.xlabel('\nDeviation from true rating')
plt.ylabel('Frequency')
plt.ylim([0,1800])
plt.text(-0.5,1600,'RMS error = 1.15',fontweight='bold',color = 'red',fontsize=35,bbox=props)

plt.subplot(122)
plt.hist(deviations, bins, alpha=.9, rwidth=0.6, color='crimson')
plt.title('Prediction = Baseline + CF')
plt.ylabel('Frequency')
plt.xlabel('\nDeviation from true rating')
plt.ylim([0,1800])
plt.text(-0.5,1600,'RMS error = 0.47',fontweight = 'bold',fontsize = 35,color = 'red', bbox = props)

#plt.hist(deviations, bins, alpha = 0.4, color = 'b', rwidth = 0.6)
#plt.hist(avgDeviations, bins, alpha=0.1, color='k', rwidth = 0.6)
#
#plt.xlabel('\nDeviation from true rating')
#plt.ylabel('Frequency')
#plt.legend(["Naive Prediction: Business Average \nRMS error = 1.03 \n", \
    #"Collaborative Filter Prediction \nRMS error = 0.81"], loc=2, frameon = 0)
#plt.ylim([0,1300])

plt.show()