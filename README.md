[![Build Status](https://travis-ci.org/futurice/file-sharing.svg?branch=master)](https://travis-ci.org/futurice/file-sharing)
File sharing service
====================

File Sharing is a simple anonymous file sharing service where users can upload any number of files and the service will automatically generate a password protected ZIP file from the content. After uploading the file, the app will give you a password and a link for the file that you can pass on to the person in need. If you’re looking for a good self-hosted solution for sharing files, you might want to try this out!

Background
----------
This application was created as an internal support system at [Futurice](http://www.futurice.com).

Installation
------------

Install requirements with `pip install -r requirements.txt`

Edit `local_settings.py`:
```bash
cd filesharing/filesharing
cp local_settings.py.template local_settings.py
# edit the file to set the Django SECRET_KEY and customize any settings
cd -
```

Run the tests: `filesharing/manage.py test filesharing/`

Run the application with `filesharing/manage.py runserver`

About Futurice
--------------
[Futurice](http://www.futurice.com) is a lean service creation company with offices in Helsinki, Tampere, Berlin and London.

Support
-------
Pull requests and new issues are of course welcome. If you have any questions, comments or feedback you can contact us by email at sol@futurice.com. We will try to answer your questions, but we have limited manpower so please, be patient with us.
