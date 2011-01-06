import os
import logging
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import mail

class MainHandler(webapp.RequestHandler):
    def get(self):
        path = self.request.path
        temp = os.path.join(os.path.dirname(__file__), 'templates' + path)
        if not os.path.isfile(temp):
            temp = os.path.join(
                os.path.dirname(__file__), 'templates/index.htm')
        outstr = template.render(temp, {'path': path})
        self.response.out.write(outstr)

    def post(self): # user submitted an email message
        path = self.request.path
        temp = os.path.join(os.path.dirname(__file__), 'templates/contact.htm')
        theDict = {'path': path}
        name = self.request.get('name')
        theDict['name'] = name
        email = self.request.get('email')
        theDict['email'] = email
        message = self.request.get('message')
        theDict['message'] = message

        if not mail.is_email_valid(email) or '@' not in email:
            error = "The email address you entered does not appear to be valid."
            theDict['error'] = error
            del theDict['email']
        elif len(name) == 0:
            theDict['error'] = "Please enter a name."
        elif len(message) == 0:
            theDict['error'] = "Please enter a message."
        if theDict.has_key('error'):
            outstr = template.render(temp, theDict)
            self.response.out.write(outstr)
            return

        sender = "arthurjwannerjr@gmail.com"
        to = "jimwanner19@yahoo.com"
        subject = "New Message posted to the C.J. Cubers website"
        message = "From: " + name + '\n' + "Email: " + email + '\n' + message
        mail.send_mail(sender, to, subject, message)
        theDict['greeting'] = "Your message has been sent, thank you!"
        outstr = template.render(temp, theDict)
        self.response.out.write(outstr)


def main():
    application = webapp.WSGIApplication([
        ('/.*', MainHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
