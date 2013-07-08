yelp_phoenix_academic_dataset-1
===============================

Personalized Yelp Recommendations

Modules:

- app.py: Flask interface to front end. Takes query and calls Recommend.py to get recommendations.
- Recommend.py: Main module. Takes user query from app.py, retrieves appropriate databases and calculates recommendations

- CalculateSimilarities.py: Calculates the similarity between two businesses according to a damped Pearson correlation.
- CalculateAllSimilarities.py: Calculate similarities between each pair of businesses in the database and stores these values into a MySQL database.

- CrossValidation_set.py: Creates a random hold out set for validation. There is a parameter here that can be toggled so that you can either choose a random set or choose random review from users with most reviews. Also adjusts the reviews database to remove these ratings.
- CrossValidate.py: Calls CrossValidation_set.py, performs prediction on the reviews in the hold out set, and calculates RMS error of predictions. Plots histograms to show error distribution.

- CreateSQL_Users.py, CreateSQL_Reviews.py, CreateSQL_Businesses.py: Create relevant SQL databases from Yelp Academic dataset.

