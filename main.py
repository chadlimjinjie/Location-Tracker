
import os
import pytz
import pymongo
import requests
from flask_cors import CORS
from datetime import datetime
from flask import Flask, current_app, jsonify, request, render_template

tz_SG = pytz.timezone('Asia/Singapore')

app = Flask(__name__)
emails = ['chadlimjinjie@gmail.com', 'codauknow@gmail.com']

CORS(app)

app.GEOAPIFY_API_KEY = os.getenv('GEOAPIFY_API_KEY')

client = pymongo.MongoClient(os.getenv('DB_URI'))
db = client.Location
collection = db['current-location']
collection.create_index('username', unique=True)

@app.route('/')
def index():
  return render_template('index.html')
  
@app.route('/PostLocation/<username>', methods=['POST'])
def PostLocation(username):
  username = username.lower()
  current_time = datetime.now(tz_SG)
  current_time = current_time.strftime('%d/%m/%Y, %I:%M:%S%p')
  
  GEOAPIFY_API_KEY = current_app.GEOAPIFY_API_KEY
  #print(request.json)
  latitude = request.json['latitude']
  longitude = request.json['longitude']
  #print(latitude)
  #print(longitude)
  # https://api.geoapify.com/v1/geocode/reverse?lat=test&lon=test&apiKey=YOUR_API_KEY
  # https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={latitude}&longitude={longitude}&localityLanguage=en
  
  response = requests.get(f'https://api.geoapify.com/v1/geocode/reverse?lat={latitude}&lon={longitude}&apiKey={GEOAPIFY_API_KEY}')
  response_data = response.json()
  response.close()
  #print(response_data)
  properties = response_data['features'][0]['properties']
  #print(properties)
  address = properties['formatted']
  print(address)

  try:
    current_location = {'username':username, 'latitude':latitude, 'longitude':longitude, 'last_seen':current_time}
    collection.insert_one(current_location)
  except Exception as e:
    query = {'username':username}
    current_location = { '$set': { 'latitude':latitude, 'longitude':longitude, 'last_seen':current_time } }
    collection.update_one(query, current_location)
  #yagmail.SMTP(os.getenv('EMAIL'), os.getenv('PASSWORD')).send(emails, 'Where is chad?', address)
  return address


@app.route('/GetLocation/<username>', methods=['GET'])  # URL with a variable
def GetUserLocation(username):    # The function shall take the URL variable as parameter
  username = username.lower()
  try:
    query = {'username':username}
    user = collection.find_one(query, {'_id': 0, 'username':1, 'latitude':1, 'longitude':1, 'last_seen':1})
    #print(type(user))
    return jsonify(user)
  except Exception as e:
    return e
  #return user

@app.route('/GetLocation', methods=['GET'])
def GetLocation():
  # Get all users posture data from the database and anonymize them
  try:
    data = []
    users = collection.find({}, {'_id': 0, 'username':1, 'latitude':1, 'longitude':1, 'last_seen':1})

    for user in users:
      data.append(user)
    
    return jsonify(data)

  except Exception as e:
    return e

if __name__ == '__main__':
  app.run("0.0.0.0", 5000)
  