from google.appengine.ext import ndb

from utils import *

class User(ndb.Model):
	"""
	A registered user
	"""

	username = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)
	email = ndb.StringProperty()
	joined = ndb.DateTimeProperty(auto_now_add=True)
	image = ndb.BlobProperty()

	@classmethod
	def create_user(cls, username, password, email=None ):

		"""
		Create a new user with the provided credentials,
		and throw an exception if something's wrong
		"""
		
		 

		if not is_username_valid(username):
			raise ValidationError("That's not a valid username.")

		user = cls.query(cls.username==username).fetch()
		if user:
			raise UserError("User already exists!")

		if not is_password_valid(password):
			raise ValidationError("That's not a valid password.")

		if email:
			if not is_email_valid(email):
				raise ValidationError("That's not a valid email.")

		new_user = cls(username=username, password=encrypt(password), email=email  ).put()
		
		return new_user.id()

	@classmethod
	def authenticate(cls, username, password):
		"""
		Check if the provided username and password are valid
		"""

		try:
			user = cls.query(cls.username==username).fetch()[0]

		except:
			raise UserError("User does not exist!")

		if user.username == username and user.password == encrypt(password):
			return str(user.key.id())
		else:
			raise AuthenticationError("Invalid username/password!")



class Post(ndb.Model):
	"""
	A blog post written by a registered user
	"""

	title = ndb.StringProperty(required=True)
	content = ndb.TextProperty(required=True)
	author = ndb.KeyProperty(kind='User', required=True)
	created = ndb.DateTimeProperty(auto_now_add=True)
	modified = ndb.DateTimeProperty(auto_now=True)
	like = ndb.IntegerProperty()
	un = ndb.IntegerProperty(repeated=True)
	comment = ndb.StringProperty(repeated=True)

	@classmethod
	def top_posts(cls):
		"""
		Returns the most recent 10 blog posts
		"""
		
		top_posts = cls.query().order(-cls.created).fetch(10)
		return list(top_posts)

	@classmethod
	def create_new(cls, title, content, user,comment ):
		"""
		Create a new blog post
		"""

		# if not title or content:
		# 	raise ValidationError("Title / content cannot be empty!")
		un1=[user.key.id()]
		post = cls(title=title, content=content, author=user.key,un =[user.key.id()], like=(len(un1)-1),comment=comment).put()

		return post.id()