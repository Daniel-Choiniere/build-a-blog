import jinja2
import os
import webapp2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                              autoescape = True)



class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)



class MainPage(Handler):
    """ Handles requests coming in to '/'
    """
    def get(self):
        t = jinja_env.get_template("welcome.html")
        content = t.render()
        self.response.write(content)




class NewPost(Handler):
    """ Handles requests coming in to '/newpost'
    """
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")

        self.render("newpost.html", title=title, art=art, error=error, arts=arts)

    def get(self):
            self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            self.redirect("/blog")
            a = Art(title = title, art = art)
            a.put()
        else:
            error = "we need both a title and a blog post!"
            self.render_front(title, art, error)



class Blog(Handler):
    """ Handles requests coming in to '/blog'
    """
    def render_entries(self, title="", entry="", error=""):
        entries = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC LIMIT 5")
        self.render("blog.html", title=title, entry=entry, error=error, entries=entries)

    def get(self):
        self.render_entries()




app = webapp2.WSGIApplication([
    ('/blog', Blog),
    ('/', MainPage),
    ('/newpost', NewPost)
], debug=True)
