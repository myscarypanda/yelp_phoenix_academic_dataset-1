# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 16:05:48 2013

@author: lisaqian
"""

import MySQLdb as db
from math import sqrt


############
#Return a list of most similar businesses for a given business (include a similarity measure)
#Each item in list is a tuple: (sim, bus_id)
def getTopMatches(BReviews, bus, n):
    #start with just random numbers
    scores = [(calcSim(BReviews, bus, other), other) for other in BReviews if other!=bus]
    scores.sort()
    scores.reverse()
    return scores[0:n]
    
############

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
