from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrapemars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/marsdb_Keturah")

# Create route that renders index.html template and finds data from mongo
@app.route("/")
def home(): 

    # Find data
    mars_data = mongo.db.mongomars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)

# Route that will trigger the scrape function
@app.route('/scrape')
def scrape():

    # Run the scrape function
    mars_data = scrapemars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mongomars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)