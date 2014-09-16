import webapp2

from utils import *

from models import User, Post

class BaseHandler(webapp2.RequestHandler):
	"""
	Base class for view functions, which provides basic rendering 
	funtionalities
	"""

	def render(self, template, **kw):
		"""
		Render a template with the given keyword arguments
		"""

		self.response.out.write(render_str(template, **kw))

	def set_secure_cookie(self, name, val):
		"""
		Set an encrypted cookie on client's machine
		"""

		cookie_val = make_secure_val(val)
		self.response.headers.add_header(
			'Set-Cookie',
			'%s=%s; Path=/' % (name, cookie_val)
			)

	def read_secure_cookie(self, name):
		"""
		Read a cookie and check it's integrity
		"""

		cookie_val = self.request.cookies.get(name)
		return cookie_val and check_secure_val(cookie_val)

	def initialize(self, *a, **kw):
		"""
		Override the constuctor for adding user information
		when a request comes
		"""

		webapp2.RequestHandler.initialize(self, *a, **kw)
		user_id = self.read_secure_cookie('user')
		self.user = user_id and User.get_by_id(int(user_id))


class Home(BaseHandler):
	"""
	Handle the homepage, which shows the 10 most recent blog posts
	"""

	def get(self):
		"""
		For a GET request, return the homepage
		"""

		top_posts = Post.top_posts()

		self.render("home.html", posts=top_posts, user=self.user, permalink=False)

		"""def post(self):"""

class mypost(BaseHandler):
	"""
	Handle the owners posts, which shows only his posts
	"""

	def get(self):
		"""
		For a GET request, return the homepage
		"""

		top_posts = Post.top_posts()

		self.render("mypost.html", posts=top_posts, user=self.user, permalink=True)


class Home1(BaseHandler):
	"""
	Handle the homepage, which shows the 10 most recent blog posts
	"""

	def get(self):
		"""
		For a GET request, return the homepage
		"""
	
		top_posts = Post.top_posts()
		self.render("home1.html", posts=top_posts, user=self.user, permalink=False)
	def post(self):

		top_posts = Post.top_posts()
		self.render("home1.html", posts=top_posts, user=self.user, permalink=False)

class Permalink(BaseHandler):
	"""
	Handle permalink for the posts
	"""

	def get(self, post_id):
		"""
		For a GET request with a valid post_id, return the post
		Else, return a 404 error
		"""

		post = Post.get_by_id(int(post_id))
		if post:
			self.render("home1.html", user=self.user, posts=[post], permalink=True)
		else:
			self.abort(404)

class likelink(BaseHandler):
	"""like++"""
	def get(self,post_id):
		flag=0
		post = Post.get_by_id(int(post_id))
		user=self.user
		uidr=user.key.id()
		for uid in post.un:
			if uidr==uid:
				flag=1
		if flag==0:
			post.like=post.like+1
			post.un.append(uidr)
			post.put()
			top_posts = Post.top_posts()
			self.render("home1.html", posts=top_posts, user=self.user, permalink=False, success="LIKED")
		else:
			top_posts = Post.top_posts()
			self.render("home1.html", posts=top_posts, user=self.user, permalink=False, success="CANT LIKE !!")


class comment(BaseHandler):
	"""adds comment to post"""
	def get(self,post_id):
		post = Post.get_by_id(int(post_id))
		user=self.user
		uidr=user.key.id()
		username=user.username
		#self.response.out(comment)
		post.comment.append(self.request.get('commentt') +" ~~~by : "+ user.username)
		post.put()
		top_posts = Post.top_posts()
		self.render("home1.html", posts=top_posts, user=self.user, permalink=False, )
		

class Login(BaseHandler):
	"""
	Handle login to the blog
	"""

	def get(self):
		"""
		For a GET request, render the login page
		"""

		user = self.user

		if user:
			self.redirect('/')

		self.render('login.html', user=user)

	def post(self):
		"""
		For a POST request, perform the login. If successful, redirect
		to homepage
		"""

		username = self.request.get('username')
		password = self.request.get('password')
		
        

		try:
			user_id = User.authenticate(username, password,)
			self.set_secure_cookie('user', str(user_id))
			self.redirect('/myhome')
		
		except Exception, e:
			self.render("login.html", user=self.user, error = e)

class Logout(BaseHandler):
	"""
	Log out a user
	"""

	def get(self):
		"""
		Log out the user and redirect her to homepage
		"""
		
		self.set_secure_cookie('user', '')
		self.redirect('/')

class Signup(BaseHandler):
	"""
	Signup a new user
	"""

	def get(self):
		"""
		Render the signup page
		"""

		user = self.user

		if user:
			self.redirect('/')

		self.render('signup.html', user=user)

	def post(self):
		"""
		Create a new user, and redirect to homepage
		"""

		username = self.request.get('username')
		password = self.request.get('password')

		try:
			user = User.create_user(username, password)
			self.render('login.html',
						success="Great! You are registered! Please log in.", user=user)

		except Exception, e:
			self.render('signup.html', error=e, user=self.user)

class NewPost(BaseHandler):
	"""
	Create a new post
	"""

	def get(self):
		"""
		Render the form for adding new post
		"""

		if not self.user:
			self.redirect('/login')

		self.render('newpost.html', user=self.user)

	def post(self):
		"""
		Add a new post, and redirect to the permalink page
		"""

		title = self.request.get('title')
		content = self.request.get('content')
		user = self.user
		comment=[]
		if not user:
			self.abort(403)

		try:
			post_id = Post.create_new(title=title, content=content, user=user ,comment=comment)
			self.redirect('/post/%s' % str(post_id))

		except Exception, e:
			self.render('newpost.html', 
						post={'title' : title, 'content' : content},
						user=self.user,
						error=e)
class delete(BaseHandler):
	def get(self, post_id):

		post = Post.get_by_id(int(post_id))
		post.key.delete()
		if post:
			#self.render("home1.html", user=self.user, posts=[post], permalink=False)
			#self.redirect('/mypost')
			top_posts = Post.top_posts()
			self.render("home1.html", posts=top_posts, user=self.user, permalink=False, success="POST DELETED SUCCESSFULLY")
		else:
			self.abort(404)
class edit(BaseHandler):
	def get(self, post_id):

		post = Post.get_by_id(int(post_id))
		if post:
			self.render('newpost1.html', 
						post={'title' : post.title, 'content' : post.content, 'id':post.key.id()},
						user=self.user)
		else:
			self.abort(404)
			
	

class NewPost1(BaseHandler):

	def post(self, post_id1):
		title = self.request.get('title')
		content = self.request.get('content')
		user = self.user
		post = Post.get_by_id(int(post_id1))
		if not user:
			self.abort(403)

		try:
			post_id = Post.create_new(title=title, content=content, user=user,comment=post.comment )
			post.key.delete()
			self.redirect('/post/%s' % str(post_id))

		except Exception, e:
			self.render('newpost.html', 
						post={'title' : title, 'content' : content},
						user=self.user,
						error=e)
					
