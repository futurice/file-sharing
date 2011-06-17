FutuShare - The Django Edition

Notes:
- Currently the templates look for static media in /futushare/...
- Most paths etc. can (and should) be changed in the settings.py
- Django does not serve the zip files, it redirects the user to the file, which is served by an http server

Known Issues:
- File size is checked after the whole file has been posted to the server, which leads to unneccesary server load.
