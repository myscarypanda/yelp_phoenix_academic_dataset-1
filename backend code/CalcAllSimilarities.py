# Calculates similarities between each pair of businesses, stores in a database
#

"""
Created on Tue Jun 11 15:10:21 2013

@author: lisaqian
"""
import MySQLdb as db
from math import sqrt
from CalcSimilarities import *





#######################
##Main function
con = db.connect(host = "localhost", user = "Lisa", passwd = 'lisa', db ="yelp", port = 3306)
with con:
    
    cur = con.cursor()
    #cur.execute('select * from JoinedReviews')
    cur.execute('select * from JoinedReviews_Two') #Reviews that come from Reviewers > 1 review, and from businesses > 7 ratings
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
    cur.execute("DROP TABLE IF EXISTS Similarities_Two")
    cur.execute("CREATE TABLE Similarities_Two(\
                num INT NOT NULL auto_increment, \
                b1_id varchar(255) NOT NULL, \
                b2_id varchar(255) NOT NULL, \
                sim FLOAT NOT NULL, \
                PRIMARY KEY(num)) ENGINE = InnoDB;")
                
    for b1 in matches: 
        for (sim, b2) in matches[b1]:
            
            cur.execute('INSERT INTO Similarities_Two(b1_id, b2_id, sim) \
                        VALUES("%s", "%s", "%f")' % (b1, b2, sim))