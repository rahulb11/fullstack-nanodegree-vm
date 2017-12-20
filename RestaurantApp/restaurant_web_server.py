from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<a href='/restaurants/new'>Make a new restaurant here</a></br></br>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href='/restaurants/%d/edit'>Edit</a></br>" % restaurant.id
                    output += "<a href='/restaurants/%d/delete'>Delete</a></br></br></br>" % restaurant.id
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/delete"):
                restaurantID = int(self.path.split("/")[2])
                selectedRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = "<html><body>"
                output += """<form method='POST' enctype='multipart/form-data' action='/restaurants/%d/delete'>
                        <h2>Are you sure you want to delete %s?</h2>
                        <input type='submit' value='Delete'>
                        </form>""" % (restaurantID, selectedRestaurant.name)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurantID = int(self.path.split("/")[2])
                selectedRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = "<html><body>"
                output += """<form method='POST' enctype='multipart/form-data' action='/restaurants/%d/edit'>
                        <h2>%s</h2>
                        <input placeholder='%s' name='updated_rest_name' type='text'>
                        <input type='submit' value='Rename'>
                        </form>""" % (restaurantID, selectedRestaurant.name, selectedRestaurant.name)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = "<html><body>"
                output += """<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                        <h2>Make a new restaurant</h2>
                        <input placeholder='New Restaurant Name' name='new_rest_name' type='text'>
                        <input type='submit' value='Create'>
                        </form>"""
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>Hello!"
                output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                        <h2>What would you like me to say?</h2>
                        <input name='message' type='text'>
                        <input type='submit' value='Submit'>
                        </form>"""
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>&#161Hola!<a href='/hello'> Back to Hello</a>"
                output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                        <h2>What would you like me to say?</h2>
                        <input name='message' type='text'>
                        <input type='submit' value='Submit'>
                        </form>"""
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                restaurantID = int(self.path.split("/")[2])
                selectedRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                session.delete(selectedRestaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Location','/restaurants')
                self.end_headers()
                return

            if self.path.endswith("/edit"):
                restaurantID = int(self.path.split("/")[2])
                selectedRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('updated_rest_name')
                if(messagecontent[0] != ''):
                    print messagecontent[0]
                    selectedRestaurant.name = messagecontent[0]
                    session.add(selectedRestaurant)
                    session.commit()
                self.send_response(301)
                self.send_header('Location','/restaurants')
                self.end_headers()
                return

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new_rest_name')
                if(messagecontent[0] != ''):
                    print messagecontent[0]
                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                self.send_response(301)
                self.send_header('Location','/restaurants')
                self.end_headers()
                return

            # self.send_response(301)
            # self.end_headers()
            # ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # if ctype == 'multipart/form-data':
            #     fields = cgi.parse_multipart(self.rfile, pdict)
            #     messagecontent = fields.get('message')
            # output = ""
            # output += "<html><body>"
            # output += "<h2>How about this:</h2>"
            # output += "<h1>%s</h1>" % messagecontent[0]
            # output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
            #             <h2>What would you like me to say?</h2>
            #             <input name='message' type='text'>
            #             <input type='submit' value='Submit'>
            #             </form>"""
            # output += "</body></html>"
            # self.wfile.write(output)
            # print output

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()