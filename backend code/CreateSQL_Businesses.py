# Imports Yelp "Businesses" data from Phoenix API. Imports into MySQL database

"""
Created on Fri Jun  7 18:07:55 2013

@author: lisaqian
"""

import MySQLdb as db
import json

#Open up the Business data set, put everything into a dataframe
path = 'yelp_academic_dataset_business.json'
bus = [json.loads(line) for line in open(path)]



#Open up connection to the Yelp MySQL database, 
con = db.connect(host = "localhost", user = "Lisa", passwd = 'lisa', db ="Yelp", port = 3306)
with con:
    
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Businesses")
    cur.execute("CREATE TABLE Businesses(\
                business_id varchar(255) NOT NULL, \
                city varchar(255) NOT NULL, \
                latitude FLOAT NOT NULL, \
                longitude FLOAT NOT NULL, \
                name varchar(255) NOT NULL,\
                review_count int NOT NULL,\
                type varchar(255) NOT NULL, \
                stars FLOAT NOT NULL, \
                category varchar(255) NOT NULL, \
                PRIMARY KEY(business_id)) ENGINE = InnoDB;")
                
    
    for i in range(len(bus)):    
        
        if len(bus[i]['categories'])>0:
            cat = bus[i]['categories'][0]
        else:
            cat = ''
        
        cur.execute('INSERT INTO Businesses(business_id, city, latitude, longitude, name, review_count, type, stars, category) \
                    VALUES("%s", "%s", "%f", "%f", "%s", "%d", "%s", "%f", "%s")' % \
                    (bus[i]['business_id'].encode('ascii','ignore'), bus[i]['city'].encode('ascii','ignore'), \
                     bus[i]['latitude'], bus[i]['longitude'], bus[i]['name'].encode('ascii','ignore'), bus[i]['review_count'], \
                     bus[i]['type'].encode('ascii','ignore'), bus[i]['stars'], cat))
                     
                     