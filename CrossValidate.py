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



##############
#Similarity measure: returns the similarity score between two businesses based on user reviews
def calcSim(BReviews, b1, b2):
    #Euclidean distance between b1 and b2
    commonUsers = [] #users who went to both b1 and b2
    
    for user in BReviews[b1]:
        if user in BReviews[b2]:
            commonUsers.append(user)
            
    n = float(len(commonUsers))
    #if no one went to both businesses, then return 0 (b1 and b2 are not similar at all)
    if n == 0:
        return 0
        
#========Euclidean distance======================================================================
#     #calculate sum of squares of distances
#     sumSqr = 0
#     for user in commonUsers:
#         dif = BReviews[b1][user] - BReviews[b2][user]
#         sumSqr += pow(dif,2)
#==============================================================================
    
    #calculate the pearson correlation coefficient
    sum1 = sum([BReviews[b1][u] for u in commonUsers])
    sum2 = sum([BReviews[b2][u] for u in commonUsers])
    
    sum1sq = sum([pow(BReviews[b1][u],2) for u in commonUsers])
    sum2sq = sum([pow(BReviews[b2][u],2) for u in commonUsers])
    
    pSum = sum([BReviews[b1][u]*BReviews[b2][u] for u in commonUsers])
    
    num = pSum - (1.0*sum1*sum2/n)
    den = sqrt((sum1sq - 1.0*pow(sum1,2)/n)*(sum2sq - 1.0*pow(sum2,2)/n))
    if den==0:
        return 0
        
    r = num/den
    
    #damp the pearson coefficient so that you need to have at least 10 common users
    coef = r*min(1, 1.0*n/10)
    return coef
    
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
        #predictedRating = 1.0*score/totalSim
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
    ratings.append(HoldOut[key])
    predictions.append(pred)
    
#rms error
rms = sqrt(sumOfSquares/len(HoldOut))
print rms

#plot histogram of the deviations
params = {'legend.fontsize': 20,
          'font.size' : 24,
          'axes.linewidth': 0.5,
          'legend.linewidth': 0.5}
plt.rcParams.update(params)
#plt.figure(figsize=(12,9))
#plt.figure(figsize=(12, 18)) 
plt.figure(figsize=(30, 10)) 
bins = np.linspace(-4, 4, 18)
#bins = np.linspace(0,4,9)

plt.subplot(121)
#plt.hist([abs(i) for i in avgDeviations], bins, alpha=.9, color='crimson')
plt.hist(avgDeviations, bins, alpha=.9, color='crimson')
plt.title('Prediction = Business Average',fontsize = 24)
plt.xlabel('Deviation from true rating')
plt.ylabel('Frequency')
#plt.ylim([0,1])
plt.ylim([0,1200])
plt.text(0.5,1000,'RMS error = 1.029',fontweight='bold',fontsize=26, color = 'crimson')

plt.subplot(122)
#plt.hist([abs(i) for i in deviations], bins, alpha=.9, color='crimson')
plt.hist(deviations, bins, alpha=.9, color='crimson')
plt.title('Prediction = CF + Baseline',fontsize = 24)
plt.ylabel('Frequency')
plt.xlabel('Deviation from true rating')
#plt.ylim([0,1])
plt.ylim([0,1200])
plt.text(0.5,1000,'RMS error = 0.811',fontweight = 'bold',fontsize = 26,color = 'crimson')

#n,bins,patches = plt.hist([[abs(i) for i in avgDeviations], [abs(j) for j in deviations]],bins,normed=1,alpha=1,histtype='step')
#
#plt.xlabel('Deviation from true rating', fontsize = 18)
#plt.ylabel('Frequency',fontsize=18)
#plt.title('Error: Prediction - True Rating',fontsize=24)
#plt.legend(["Prediction = Business Average \nRMS error = 1.029 \n\n", \
    #"Prediction = CF + Baseline \nRMS error = 0.811"], loc=1)
plt.show()