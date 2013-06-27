# Calculates similarities between each pair of businesses, stores in a database
#

"""
Created on Tue Jun 11 15:10:21 2013

@author: lisaqian
"""
import MySQLdb as db
from math import sqrt


#############################
#Business comparison dataset: Find the top n most similar businesses for each business
#INPUT: BReviews: BusinessReviews - dictionary of each business and the reviews it got
#OUTPUT: matches: dectionary of each business and its most similar businesses
def calcSimilarBusinesses(BReviews, n = 50):
    
    #Dictionary of businesses, where value is a list of top n businesses most similar to each b
    #each entry of list is a tuple: (score, business_id)
    matches = {}

    for business in BReviews:
        scores = getTopMatches(BReviews, business, n=n)
        matches[business] = scores
    
    return matches

#############################


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



#######################
##Main function
con = db.connect(host = "localhost", user = "Lisa", passwd = 'lisa', db ="Yelp", port = 3306)
with con:
    
    cur = con.cursor()
    #cur.execute('select * from JoinedReviews')
    cur.execute('select * from JoinedReviews_Small')
    allReviews = cur.fetchall() #these are all the reviews from JoinedReviews, as tuples
    
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
    
    BusinessReviews.setdefault(business_id,{})
    UserReviews.setdefault(user_id,{})
    BusinessReviews[business_id][user_id] = star
    UserReviews[user_id][business_id] = star
    
    #Determine where in the utility matrix the rating should go:
    if business_id not in BusinessLookup: 
        #this business is not yet in our dictionary
        column = bi
        #place this business into the business lookup table
        BusinessLookup[business_id] = [column, rev[3], rev[4]]
        
        bi += 1 #increment the index for last business recorded

    if user_id not in UserLookup:
        row = ui
        #place this user into the user lookup table
        UserLookup[user_id] = [row, rev[7], rev[8]]
        ui+=1

for business in BusinessReviews:
    scores = getTopMatches(BusinessReviews, business, n=50)
    matches[business] = scores


with con:
#Put these similarities back into the database in a table called similarities
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Similarities")
    cur.execute("CREATE TABLE Similarities(\
                num INT NOT NULL auto_increment, \
                b1_id varchar(255) NOT NULL, \
                b2_id varchar(255) NOT NULL, \
                sim FLOAT NOT NULL, \
                PRIMARY KEY(num)) ENGINE = InnoDB;")
                
    for b1 in matches: 
        for (sim, b2) in matches[b1]:
            
            cur.execute('INSERT INTO Similarities(b1_id, b2_id, sim) \
                        VALUES("%s", "%s", "%f")' % (b1, b2, sim))