# Imports Yelp "Reviews" data from Phoenix API. Imports into MySQL database

"""
Created on Fri Jun  7 18:07:55 2013

@author: lisaqian
"""

import MySQLdb as db
import json
import pandas

#Open up the Reviews data set, put everything into a dataframe
path = 'yelp_academic_dataset_review.json'
reviews = [json.loads(line) for line in open(path)]
#reviewsDF = DataFrame(reviews)


#Open up connection to the Yelp MySQL database, 
con = db.connect(host = "localhost", user = "Lisa", passwd = 'lisa', db ="Yelp", port = 3306)
with con:
    
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Reviews")
    cur.execute("CREATE TABLE Reviews(business_id varchar(255) NOT NULL, \
                date date NOT NULL, \
                review_id varchar(255) NOT NULL, \
                stars int NOT NULL, \
                type text NOT NULL, \
                user_id varchar(255) NOT NULL, \
                PRIMARY KEY(review_id)) ENGINE = MyISAM;")
                
    
    for i in range(len(reviews)):    
        cur.execute('INSERT INTO Reviews(business_id, \
                    date, review_id, stars, type, user_id) \
                    VALUES("%s", "%s", "%s", "%d", "%s", "%s")' % \
                    (reviews[i]['business_id'].encode('ascii','ignore'), reviews[i]['date'].encode('ascii','ignore'), \
                    reviews[i]['review_id'].encode('ascii','ignore'), reviews[i]['stars'], \
                    reviews[i]['type'].encode('ascii','ignore'), reviews[i]['user_id'].encode('ascii','ignore')))
                    
                    
cur.close()
con.close()