import cherrypy
import random


class AdLib(object):
    @cherrypy.expose
    def index(self):

        # Set the media type
        cherrypy.response.headers['Content-Type'] = 'text/html'

        # Create some random lists to choose from
        career_list = ["Disney princess", "astronaut", "doctor", "superstar", "teacher", "application developer"]
        # Make the choices
        career = random.choice(career_list)

        # Print out the heading in HTML <h1> tags
        result = "<h1>Random Story Generator</h1>"

        # Write our story
        result += f"<p>When I graduate, I want to be a(n) {career}!</p>"

        # Return the result
        return result


cherrypy.quickstart(AdLib())
