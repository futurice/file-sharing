from os import path, makedirs, listdir
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.validators import email_re
from django.core.mail import send_mail
import subprocess, random, string, urllib2, smtplib, re, shutil, mimetypes
from futuShareDjango.settings import UPLOAD_DIRECTORY, ZIP_URL, MAX_UPLOAD_FILE_SIZE, SERVER_ROOT_ADDRESS, PASSWORD_LENGTH, FREE_ZIP_DIR
from futuUpload.models import Zip

#The root folder for the files:
upload_dir = UPLOAD_DIRECTORY

#Folder to store the zips
zip_dir = FREE_ZIP_DIR


# Renders the frontpage
def index(request):
	return render_to_response('futuUpload/base.html')


# This method saves a file posted to it in the directory specified in the settings
def upload(request, folder):
	if request.method == 'POST':
	
		for field_name in request.FILES:
			uploaded_file = request.FILES[field_name]
			
			if uploaded_file.size > MAX_UPLOAD_FILE_SIZE:
				return HttpResponse('File was too big.')

			# Create folder
			dir = upload_dir + folder + '/'
			if not path.exists(dir):
				makedirs(dir)

			# Save to folder
			destination_path = dir + uploaded_file.name
			destination = open(destination_path, 'wb+')
			for chunk in uploaded_file.chunks():
				destination.write(chunk)
			destination.close()
			
		return HttpResponse('DONE')
	
	else:
		return HttpResponseNotFound()
	
	#Redirect the user to the address specified in ZIP_URL
	#This is used for old password protected zip files
def getzip(request, zip):
	return HttpResponseRedirect(ZIP_URL + zip)
	
	
	#Zip the files in the folder specified in the arguments and save
	#the zip to the path defined in the settings
def zip(request, folder):
	
	if request.method == 'POST':
		N = PASSWORD_LENGTH
		
		#Hard to remember password
		#password = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))

		#Easier to remember password
		p = subprocess.Popen(["pwgen", str(N), "1"], stdout=subprocess.PIPE)
		(password, _) = p.communicate()
		password = password.replace("\n", "")

	
		#Generate list of files
		try:
			files = []
			for file in listdir(upload_dir + folder + '/'):
				files.append(upload_dir + folder + '/' + file)
		except:
			return HttpResponseRedirect('/');
	
		#Path for the zip	
		path = zip_dir + folder + '.zip'

		#Zip it! using 7zip
		#arguments = ['/usr/bin/7z', 'a', '-p'+password, '-y', path] + files
		#zip7z = subprocess.call(arguments)

		#Zip it! using zip
		arguments = ['/usr/bin/zip', '-j', '-y', path] + files
		zip7z = subprocess.call(arguments)

		#Was the zipping successful?
		if not zip7z:
				#Remove the individual files
				shutil.rmtree(upload_dir + folder + '/')

				z = Zip(filename=folder+'.zip', password=password)
				z.save()
		
				return render_to_response('futuUpload/base_done.html', {'file': folder + '.zip',
							'password': password, 'link': SERVER_ROOT_ADDRESS + 'ask/' + folder + '.zip'})
		else:
			print 'Something went wrong while trying to zip the files. Make sure zip is installed and working.'
			print 'zip exit code: %d' % zip7z
			print " ".join(arguments)
			
			return HttpResponseServerError()
		
	else:
		#If you try something other than POST, you are redirected to the front page
		return HttpResponseRedirect('/');
	

	#Send an email and an sms to the specified addresses
def send(request):

	if request.method == 'POST':
		
		post = request.POST;

		#Get the variables from the post
		email = post.__getitem__('email')
		phone = post.__getitem__('phone')
		password = post.__getitem__('password')
		filename = post.__getitem__('file')		
			
		#Validate mail and phone
		if not email_re.match(email):
			return HttpResponse('BADEMAIL');
	
		if re.match("\+(\d+)$", phone) == None:
			return HttpResponse('BADPHONE');
	
	
		#Send SMS
		sms = urllib2.quote('Your password is "' + password + '". You should receive a mail, with the link to the file, shortly. Br, Futurice')
	
		smsurl = 'https://backupmaster2.futurice.com:13013/cgi-bin/sendsms?username=kanneluser&password=df89asj89I23hvcxSDasdf3298jvkjc839&to=' + phone + '&text=' + sms

		response = urllib2.urlopen(smsurl)
		html = response.read()
		if (html != '0: Accepted for delivery'):
			return HttpResponse('SMSFAIL')						
	
		#Send Email
		email_body = 'Hi,\n\nWe have a new file for you:\n' + SERVER_ROOT_ADDRESS + 'ask/' + filename + '\n\nWe have sent the password, for the file, to your mobile.\n\nBr, Futurice'
	
		from_addr = 'noreply@futurice.com'
		subject = 'New file on Futurice file transferring server'
		reply_addr = 'it@futurice.com'
	
		try:
			send_mail(subject, email_body, from_addr, [email], fail_silently=False)
		except:
			return HttpResponse('EMAILFAIL')
	
		return HttpResponse('DONE')
	else:
		return HttpResponseNotFound()
	

def passwordCheck(request, requestedFilename):

	#Check if we're posting the password
	if request.method == 'POST':
		post = request.POST;

		#Get the variables from the post
		requestPass = post.__getitem__('password')
		requestFile = post.__getitem__('filename')

		#If there is no such file, 404
		f = get_object_or_404(Zip, filename=requestFile)

		#Is the password correct?
		if f.isCorrectPassword(requestPass):
			
			#Serve file
			mimetypes.init()
			try:
        			filePath = FREE_ZIP_DIR + '/' + requestFile
        			fileSocket = open(filePath,"r")
        			fileName = path.basename(filePath)
        			mime_type_guess = mimetypes.guess_type(fileName)

       				if mime_type_guess is not None:
            				response = HttpResponse(fileSocket, mimetype=mime_type_guess[0])
        				response['Content-Disposition'] = 'attachment; filename=' + fileName     
       
    			except IOError:
        			return render_to_response('futuUpload/base_ask.html', {'filename': requestedFilename, 'status' : 'There was an error reading the file.'})

    			return response

		else:
			return render_to_response('futuUpload/base_ask.html', {'filename': requestedFilename, 'status' : 'Wrong password.'})
	
	#If we're not posting, the password prompt page is shown
	else:
		p = get_object_or_404(Zip, filename=requestedFilename)
    		return render_to_response('futuUpload/base_ask.html', {'filename': requestedFilename})
