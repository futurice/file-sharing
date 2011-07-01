DEBUG = True

ROOT_URLCONF = 'futuShareDjango.devurls'

STATIC_URL = "/static/"

#FUTUSHARE SETTIGNS

#Directory for storing the files before the zipping
UPLOAD_DIRECTORY = '/tmp/'

#Directory for storing the zips
ZIP_DIRECTORY = '/var/www/futushare/zip/'

#The root url for the zip files
#This is where django redirects the user to the zip
ZIP_URL = 'http://localhost/zips/'

#Django server root e.g. http://share.futurice.com/
#This is used in the visible zip links e.g. http://share.futurice.com/12345678.zip
SERVER_ROOT_ADDRESS = 'http://localhost:8000/'
