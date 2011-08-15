from flask import Flask, jsonify, request, json
from mongokit import Connection, Document

# configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

# create the application object
app = Flask(__name__)
app.config.from_object(__name__)

# connect to the database
connection = Connection(app.config['MONGODB_HOST'],
						app.config['MONGODB_PORT'])

# set db name
db = connection['test-py']

# create default user
@app.route('/add_user')
def add_user():
	user = db.users.User()
	user['name'] = u'jess'
	user['email'] = u'jess@localhost'
	user.save()
	return jsonify(username=user.name,
				   email=user.email)

# add a new favorite location
@app.route('/add_favorite', methods=['POST'])
def add_favorite():
	user = db.users.find_one({'name': u'jess'})
	if user is None:
		return jsonify(message='No user exists')
	else:
		favLoc = request.json['favorite_location']
		favorite = Favorite()
		favorite['name'] = favLoc['name']
		favorite['location'] = favLoc['location']
		favorite.save
		user['favorites'].append(favorite)
		db.users.save(user)
		return jsonify(message='Location saved.')

@app.route('/list_favorites')
def list_favorites():
	user = db.users.find_one({'name': u'jess'})
	if user is None:
		return jsonify(message='No user exists')
	else:
		return jsonify(favorites=user['favorites'])


# Models

class Favorite(Document): 
	use_autorefs = True 
	structure = { 
	  "name": unicode, 
	  "location": unicode, 
	}
	use_dot_notation = True

# register the Favorite document with our current connection
connection.register([Favorite])

class User(Document):
	use_autorefs = True 
	structure = {
		'name': unicode,
		'email': unicode,
		'favorites': [Favorite]
	}

	use_dot_notation = True
	def __repr__(self):
		return '<User %r>' % (self.name)

# register the User document with our current connection
connection.register([User])

if __name__ == '__main__':
	app.run(host='0.0.0.0')
	# app.run(debug=True)






