# Cross Validation for the recommendation algorithm - randomly select k ratings to hold out.
# Calculate rms error between predicted and actual ratings.

"""
Created on Mon Jun 17 10:18:43 2013

@author: lisaqian
"""

from Recommend import *
import numpy as np
from math import sqrt
import CalcSimilarities as cs
from CrossValidation_set import *
import matplotlib.pyplot as plt



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
        sim = cs.calcSim(BReviews, business_id, b)
        
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
        #predictedRating = 1.0*score/totalSim
        predictedRating = (mu+userBaseline+businessBaseline)+1.0*score/totalSim
        #predictedRating = (mu+businessBaseline+userBaseline)       
        
    if predictedRating > 5:
        predictedRating = 5
    elif predictedRating < 1:
        predictedRating = 1

    return predictedRating
    
    
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

#FOLLOWING DATA STRUCTURES FROM CrossValidation_set
#BReviews_HO: BusinessReviews minus the items from the holdout set
#HoldOut: {(user, business): Actual Rating}

#for each review in hold out, calculate predicted rating
for key in HoldOut.keys():
    user = key[0]
    business = key[1]
    pred = predictRating(user, business, BReviews_HO)
    error = pred - HoldOut[key]
    deviations.append(error)
    sumOfSquares += pow(error,2)
    ratings.append(HoldOut[key])
    predictions.append(pred)
    
#rms error
rms = sqrt(sumOfSquares/len(HoldOut))
print rms

#plot histogram of the deviations
plt.figure(figsize=(12, 9)) 
n, bins, patches = plt.hist(ratings, 5, normed=1, facecolor='blue', alpha=0.75)
#plt.axis([-4.0, 4.0, 0, 0.80])
#plt.axis([1, 5, 0, 0.80])
#plt.xlabel('Deviation from true rating',fontsize=16)
plt.xlabel('# of stars',fontsize=16)
plt.xticks([1,2,3,4,5],fontsize=16)
plt.yticks(fontsize=16)
plt.ylabel('Frequency',fontsize=16)
plt.title('True Rating',fontsize=20)
#plt.figtext(0.2,0.8,'RMS error = 1.029', fontsize = 20)
#plt.figtext(0.2,0.8,'RMS error = 0.811', fontsize = 20)
plt.show()
