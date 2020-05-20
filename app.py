import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo

if os.path.exists("env.py"):
    import env

# Create instance of flask and assign it to "app"
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("connection_string")

# Assign the database collection to the variable "coll"
coll = PyMongo(app).db.trailers 

# Landing page
@app.route('/') 
@app.route('/first_function')
def first_function():
    return render_template("index.html", docs = coll.find())

# Search page
@app.route('/search_terms', methods=['POST'])
def search_terms():
    terms_to_search = request.form.get('user_search')
    coll.create_index([ ('title' , 'text')])
    results = coll.find({"$text": {"$search": terms_to_search}})
    return render_template("search_results.html", results = results)

# Add trailer
@app.route('/insert_task', methods=['POST'])
def insert_trailer():
    coll.insert_one(request.form.to_dict())
    return redirect(url_for('first_function'))

if __name__ == '__main__':  
    app.run(host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", "5000")), debug=True) # Remove dubug=True before publishing