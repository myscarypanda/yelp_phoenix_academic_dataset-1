from contextlib import closing
from flask import *
from Recommend import *
import os
import random

app = Flask(__name__)

app.debug = True
app.secret_key = os.urandom(100)

@app.route("/")
def hello():
    return render_template('index.html')
    
@app.route('/slides')
def slides():
    return render_template('Slides.html')
    
@app.route('/algorithm')
def algorithm():
    return render_template('algorithm.html', title = "About")

@app.route('/validation')
def Cross():
    return render_template('validation.html')

@app.route("/query.html", methods = ['POST'])
def query():
    session['user'] = request.form['user']
    return redirect(url_for('recomm'))


@app.route("/recomm")
def recomm():
    n = 5
    
    sortedUsers = sorted(UserLookup)
    user = session['user']
    user_name = user
    
    if user == 'Jared':
        user_id = sortedUsers[1672]
    elif user == 'Jeffrey':
        user_id = sortedUsers[6875]
    elif user == 'Cassie':
        user_id = sortedUsers[18143]
    elif user == 'Steve':
       user_id = sortedUsers[13616]
    elif user == 'Lorelai':
        user_id = sortedUsers[1019]
    elif user == 'Jessica':
        user_id = sortedUsers[9437]
    elif user == 'Michael':
        user_id = sortedUsers[17007]
    elif user == 'Jay':
        user_id = sortedUsers[4295]
    else:

        #number = random.randrange(0, 22982) - from JoinedReviews_Small
        number = random.randrange(0, 21572)
        user_id = sortedUsers[number]
        user_name = UserLookup[user_id][1]
        
    avg_rating = UserLookup[user_id][2] #avg star rating for this user
    bus_ids = UserReviews[user_id] #the business ids and ratings for all businesses reviewed by user
    numReviews = len(bus_ids) #number of reviews user has
    
    reviews = {} #dictionary of reviews for user
    
    for id in bus_ids.keys():
        bus = BusinessLookup[id][1]
        rating = BusinessReviews[id][user_id]
        reviews[bus] = rating

    #Get recommendations (top 5 and bottom 5)
    rec = getRecom(UserReviews, matches, user_id, n=n)


    return render_template('recommend.html', user = user_name, avgRating = avg_rating, \
                        numRevs = numReviews, rev = reviews, rec = rec[:n], nonrec = rec[n:2*n], mostDev = rec[-n:], n = n)

if __name__ == "__main__":
    app.run('0.0.0.0', port=80)
    
#    app.run()
