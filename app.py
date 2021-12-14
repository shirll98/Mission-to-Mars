# this is where we will use Flask and mongo to begin creating Robin's web app 


# use flask to render a template, redirect a URL, create URL 
from flask import Flask, render_template, redirect, url_for
# use pymongo to interact with mongo 
from flask_pymongo import PyMongo
# use the scraping code, which we converted from jupyter notebook to python 
import scraping
app = Flask(__name__)

# telling python how to connect to mongo using pymongo 
# Use flask_pymongo to set up mongo connection

# tells python that our app will connect to mongo using URI 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for html page 
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# this function links our visual representation of our work, web app, to the code 
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   # update the db using .update() 
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)
   # {} allows insertion of json data 
   # query parameter json data will replace this 

# set up scraping route, route = 'button' of the web app 
if __name__ == "__main__":
   app.run()