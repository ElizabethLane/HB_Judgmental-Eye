"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Movie
from model import Rating

from model import connect_to_db, db
from server import app

from datetime import datetime


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|") #unpacking the data

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movies"

    Movie.query.delete()

    for row in open("seed_data/u.item"):
        #Strips the white space on the right side of the data. 
        row = row.rstrip()
        #Creates a list by splitting on the pipe. 
        movie_info = row.split("|")
        
        #Indexes the pipe to assign to desired variables. 
        movie_id = movie_info[0]
        title = movie_info[1]
        title = title[:-7] #Gets rid of the date (1995) AND the space after the last word in the title. 
        date = movie_info[2]
        imdb_url = movie_info[4]

        #Checks if there is a date, if so, changes the string to a 
        #datetime object. If not there, sets to None. 
        if date:
            released_at = datetime.strptime(date, "%d-%b-%Y")
        else:
            released_at = None

        #Instantiating an object of the class Movie, assigning the data
        #points that we extracted from the data file to each of the 
        #attributes on the object from Movie class. 
        movie = Movie(movie_id=movie_id,
                    title=title,
                    released_at=released_at,
                    imdb_url=imdb_url)

        #Adds the row to the table. 
        db.session.add(movie)

    #Adds all rows to the database
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    Rating.query.delete()

    for row in open('seed_data/u.data'):
        row = row.rstrip()
        ratings_info = row.split("\t") # Parsing the line
        #needed to be split on a tab (\t) as opposed to space.
        
        user_id = ratings_info[0]
        movie_id = ratings_info[1]
        score = ratings_info[2]

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)

        db.session.add(rating)

    db.session.commit()




def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
