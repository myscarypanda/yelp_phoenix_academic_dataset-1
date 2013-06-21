# Imports Yelp "Users" data from Phoenix API. Imports into MySQL database

"""
Created on Fri Jun  7 18:07:55 2013

@author: lisaqian
"""

import MySQLdb as db
import json

#Open up the Reviews data set, put everything into a dataframe
path = 'yelp_academic_dataset_user.json'
users = [json.loads(line) for line in open(path)]



#Open up connection to the Yelp MySQL database, 
con = db.connect(host = "localhost", user = "Lisa", passwd = 'lisa', db ="Yelp", port = 3306)
with con:
    
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Users")
    cur.execute("CREATE TABLE Users(average_stars FLOAT NOT NULL, \
                name varchar(255) NOT NULL, \
                review_count int NOT NULL, \
                type text NOT NULL, \
                user_id varchar(255) NOT NULL, \
                PRIMARY KEY(user_id)) ENGINE = InnoDB;")
                
    
    for i in range(len(users)):    
        cur.execute('INSERT INTO Users(average_stars, \
                    name, review_count, type, user_id) \
                    VALUES("%f", "%s", "%d", "%s", "%s")' % \
                    (users[i]['average_stars'], str(users[i]['name']), \
                     users[i]['review_count'], str(users[i]['type']), str(users[i]['user_id'])))