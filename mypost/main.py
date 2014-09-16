import webapp2

from config import *

app = webapp2.WSGIApplication([
								('/?', 'views.Home'),
								('/myhome', 'views.Home1'),
								('/myhome2', 'views.Home1'),
								('/mypost', 'views.mypost'),
								('/post/([0-9]+)/?', 'views.Permalink'),
								('/login/?', 'views.Login'),
								('/logout/?', 'views.Logout'),
								('/signup/?', 'views.Signup'),
								('/newpost/?', 'views.NewPost'),
								('/newpost1/([0-9]+)/?', 'views.NewPost1'),
								#('/delete/([a-z0-9/=/&/?]+)?', 'views.delete')
								('/delete/([0-9]+)/?', 'views.delete'),
								('/edit/([0-9]+)/?', 'views.edit'),
								('/like/([0-9]+)/?', 'views.likelink'),
								('/comment/([0-9]+)/?', 'views.comment')
							], debug=True)