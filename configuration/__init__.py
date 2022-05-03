from app import app
import urllib
import os

# secret key for user session
app.secret_key = "ITSASECRET"

#setting up mail
app.config['MAIL_SERVER']='smtp.corp.janusresearch.com' #mail server
app.config['MAIL_PORT'] = 25 #mail port
app.config['MAIL_USERNAME'] = 'noreply@janusresearch.com' #email
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') #password
app.config['MAIL_USE_TLS'] = False #security type
app.config['MAIL_USE_SSL'] = False #security type

#database connection parameters
connection_params = {
    'user': 'flaskdb_user',
    'password': os.environ.get('DB_PASSWORD'),
    'host': 'cluster0.xrgdk.mongodb.net',
    'port': '27017',
    'namespace': 'myFirstDatabase',
}
#PyBytesToken
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1Ijoic2NvdHQubWFydGluQGphbnVzcmVzZWFyY2guY29tIiwidCI6IjZiZGI3MGJlNmQ3YzQyZmI4MDg0YTYyMGJiMDFhZjIyIn0.IB85Stw0heASAuXqAaW6AdjNA4bNgr3kbWQer57xNLk


#HzZnJUgDiDkQ6dc3