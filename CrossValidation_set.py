
# Cross Validation for the recommendation algorithm - randomly select k ratings to hold out.
# Calculate rms error between predicted and actual ratings.

"""
Created on Mon Jun 17 10:18:43 2013

@author: lisaqian
"""

import random as rd
from math import sqrt
import copy
from Recommend import *


    
########################################
###MAIN FUNCTION: CREATE HOLDOUT SET####
#######################################
#Create the holdout set by randomly selecting a review made by a user who has a lot of reviews (>15)
#Remove this review from BusinessReviews.
#Choosing only users >15 reviews gives hold out set of 2166 reviews (1.3%)

#Make new dictionary of reviews that businesses have, so that the hold out set is removed.
#--- BReviews_HO
HoldOut = {}
BReviews_HO = copy.deepcopy(BusinessReviews)
deviations_CF = []
deviations_BA = []
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
