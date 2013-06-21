# Imports data from MySQL into dataframe.
# Then go line by line and populate utility matrix

"""
Created on Tue Jun 11 15:10:21 2013

@author: lisaqian
"""
import MySQLdb as db
import numpy as np
import random as rd
from math import sqrt




############################
#Gets a recommendation for a user
#INPUT: UReviews: UserReviews (dictionary of all the reviews users have made)
#       matches: for each business, a list of similar businesses and their similarities
#       user: user_id

def getRecom(UReviews, matches, user, n):
    
    mu = 3.7972 #avg rating for all businesses (global baseline)
    
    userBaseline = UserLookup[user][2] - mu #user baseline
    
    userRatings = UReviews[user] #these are all the ratings that user has reviewed
    scores = {} #dictionary of predicted ratings and corresponding business 
    totalSim = {}
    busBaseline= {}
    
    #iterate over items rated by the user
    for (business, rating) in userRatings.items():
        
        #business baseline (for businesses rated by user)
        bBase = BusinessLookup[business][2] - mu

        #now iterate over similar businesses
        for (sim, b2) in matches[business]:
            
            if b2 not in userRatings:
                scores.setdefault(b2,0)
                scores[b2] += 1.0*sim*(rating - (mu+ userBaseline+bBase))
                
                #sum of all the similarities
                totalSim.setdefault(b2,0)
                totalSim[b2]+=1.0*sim
                
                #business baseline
                busBaseline.setdefault(b2,0)
                busBaseline[b2] = BusinessLookup[b2][2] - mu
                
     #find average predicted ratings  

    predictedRatings = [((mu+userBaseline+busBaseline[b]) + 1.0*score/totalSim[b], BusinessLookup[b][1:]) \
                            if totalSim[b]>0 else (mu+userBaseline+busBaseline[b], BusinessLookup[b][1:]) for b, score in scores.items()]
    predictedRatings.sort()
    predictedRatings.reverse()
    
    limit5Stars = [(5.0,bus) if stars>5 else (float('%.2f' %stars),bus) for (stars,bus) in predictedRatings]
    predictedRatings = limit5Stars
    print 'length'+str(len(predictedRatings))
    print (predictedRatings[:n]+predictedRatings[-n:])
    
    if len(predictedRatings)<2*n:
        n=len(predictedRatings)/2
    
    
    return predictedRatings[:n]+predictedRatings[-n:]
    
##########################

#
#
#
#
#
#

#######################
##Main function
con = db.connect(host = "localhost", user = "Lisa", passwd = 'lisa', db ="Yelp", port = 3306)
with con:
    
    cur = con.cursor()
    #cur.execute('select * from JoinedReviews')
    cur.execute('select * from JoinedReviews_Small')
    allReviews = cur.fetchall() #these are all the reviews from JoinedReviews, as tuples
    
    #retrieve the similarities
    cur.execute('select * from Similarities order by b1_id')
    sims = cur.fetchall()
    
#Now iterate through tuples and populate the following data structures:
#   BusinessLookup -- {business_id: [pos, name, avg_stars]}
#   UserLookup -- {user_id: [pos, name, avg_stars]}
#       pos = location in the Utility matrix.

BusinessLookup = {} #Lookup table for business_id -> business name
UserLookup = {} #Lookup table for user_id -> user name
UserReviews = {} #Reviews each user made
BusinessReviews = {} #Reviews for each business
matches = {} #top matches for each business


#indices for row (business) and column (user)
bi = 0
ui = 0

for rev in allReviews:
    star = int(rev[1]) 
    business_id = rev[2]
    user_id = rev[6]
    
    #Determine where in the utility matrix the rating should go:
    if business_id not in BusinessLookup: 
        #this business is not yet in our dictionary
        column = bi
        #place this business into the business lookup table
        BusinessLookup[business_id] = [column, rev[3], rev[4]]
        
        bi += 1 #increment the index for last business recorded
        BusinessReviews[business_id] = {}
        BusinessReviews[business_id][user_id] = star
        
    else:
        #this business has already been recorded in the lookup table
        column = BusinessLookup.get(business_id)[0]
        BusinessReviews[business_id][user_id] = star
        
    if user_id not in UserLookup:
        row = ui
        #place this user into the user lookup table
        UserLookup[user_id] = [row, rev[7], rev[8]]
        ui+=1
        UserReviews[user_id] = {}
        UserReviews[user_id][business_id] = star
        
    else:
        #this user has already been recorded in the lookup table
        row = UserLookup.get(user_id)[0]
        UserReviews[user_id][business_id] = star
    

for item in sims:
    b1 = item[1]
    b2 = item[2]
    sim = item[3]
    if b1 in matches:
        matches[b1].append((sim,b2))
    else:
        matches[b1] = [(sim, b2)]


