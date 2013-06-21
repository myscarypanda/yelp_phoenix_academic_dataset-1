
# Cross Validation for the recommendation algorithm - randomly select k ratings to hold out.
# Calculate rms error between predicted and actual ratings.

"""
Created on Mon Jun 17 10:18:43 2013

@author: lisaqian
"""

from Recommend import *
import numpy as np
import random as rd
from math import sqrt
import CalcSimilarities as cs
import matplotlib.pyplot as plt
import copy


#This function calculates the predicted rating User will give a Business
#INPUT: user_id, business_id
#OUTPUT: double predictedRating
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
        predictedRating = (mu+userBaseline+businessBaseline)
        print 'zero'
    else:
        #predictedRating = 1.0*score/totalSim
        predictedRating = (mu+userBaseline+businessBaseline)+1.0*score/totalSim
        #predictedRating = (mu+userBaseline+businessBaseline)       
        
    if predictedRating > 5:
        predictedRating = 5
    elif predictedRating < 1:
        predictedRating = 1

    return predictedRating


    
########################################
###MAIN FUNCTION: CREATE HOLDOUT SET####
#######################################
#Create the holdout set by randomly selecting a review made by a user who has a lot of reviews (>15)
#Remove this review from BusinessReviews.
#Choosing only users >15 reviews gives hold out set of 2166 reviews (1.3%)
HoldOut = {}
BReviews_HO = copy.deepcopy(BusinessReviews)
deviations = []
ratings = []
predictions = []
sumOfSquares = 0


for user in UserReviews:

    #hold out a review from the most prolific reviewers so as to not disturb the utility matrix too much
    if len(UserReviews[user]) > 15:
        
        #take a random review and put in hold out set.
        business = rd.choice(UserReviews[user].keys())
        
        #check if we have already included this rating in the hold out set
        if (user,business) not in HoldOut:
            rating = UserReviews[user][business]
            HoldOut[(user,business)] = rating
            
            #remove this rating from BReviews_HO
            del BReviews_HO[business][user]

#for each review in hold out, calculate 
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
plt.hist(deviations)