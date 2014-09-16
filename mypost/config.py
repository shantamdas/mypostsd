import os
import jinja2

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
								autoescape=True)

SECRET = "gfyf6s$^&gsbb78bcasb1537hh6sd8sf66ab88"