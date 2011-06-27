from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response
from os import path, makedirs, listdir
from email.MIMEText import MIMEText
from futuShareDjango.settings import UPLOAD_DIRECTORY, ZIP_DIRECTORY, ZIP_URL, MAX_UPLOAD_FILE_SIZE, SERVER_ROOT_ADDRESS
import subprocess, random, string, urllib2, smtplib, re, shutil

#The root folder for the files:
upload_dir = UPLOAD_DIRECTORY

#Folder to store the zips
zip_dir = ZIP_DIRECTORY


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
def getzip(request, zip):
	return HttpResponseRedirect(ZIP_URL+zip)
	
	
	#Zip the files in the folder specified in the arguments and save
	#the zip to the path defined in the settings
def zip(request, folder):
	
	if request.method == 'POST':
		N=6 #Length of password
		password =  ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))
	
		#Generate list of files
		try:
			files = []
			for file in listdir(upload_dir+folder+'/'):
				files.append(upload_dir + folder + '/' + file)
		except:
			return HttpResponseRedirect('/');
	
		#Path for the zip	
		path = zip_dir+folder+'.zip'

		#Zip it! using 7zip
		#arguments = ['/usr/bin/7z', 'a', '-p'+password, '-y', path] + files
		#zip7z = subprocess.call(arguments)

		#Zip it! using zip
		arguments = ['/usr/bin/zip', '-j', '-P'+password, '-y', path] + files
		zip7z = subprocess.call(arguments)

		if not zip7z:
				#Remove the individual files
				shutil.rmtree(upload_dir+folder+'/')
		
				return render_to_response('futuUpload/base_done.html', {'file': folder+'.zip',
							'password': password, 'link': SERVER_ROOT_ADDRESS+folder+'.zip'})
		else:
			print 'Something went wrong while trying to zip the files. Make sure 7z is installed and working.'
			print '7z exit code: %d' % zip7z
			print " ".join(arguments)
			
			return HttpResponseServerError()
		
	else:
		#If you try something other than POST, you are redirected to the front page
		return HttpResponseRedirect('/');
	
	#Send an email and an sms to the specified addresses
def send(request, file, email, phone, password):
	
	#Validate mail and phone
	if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,4}|[0-9]{1,3})(\\]?)$", email) == None:
		return HttpResponse('BADEMAIL');
	
	if re.match("\+(\d+)$", phone) == None:
		return HttpResponse('BADPHONE');
	
	
	#Send SMS
	sms = urllib2.quote('Your password is "'+password+'". You should receive a mail, with the link to the file, shortly. Br, Futurice')
	
	smsurl = 'https://backupmaster2.futurice.com:13013/cgi-bin/sendsms?username=kanneluser&password=df89asj89I23hvcxSDasdf3298jvkjc839&to='+phone+'&text='+sms

	response = urllib2.urlopen(smsurl)
	html = response.read()
	if (html != '0: Accepted for delivery'):
		return HttpResponse('SMSFAIL')						
	
	#Send Email
	email_body = 'Hi,\n\nWe have a new file for you:\n'+SERVER_ROOT_ADDRESS+file+'\n\nWe have sent the password, for the file, to your mobile.\n\nBr, Futurice'
	
	from_addr = 'noreply@futurice.com'
	msg = MIMEText(email_body)
	msg['Subject'] = 'New file on Futurice file transferring server'
	msg['From'] = from_addr
	msg['Reply-to'] = 'it@futurice.com'
	msg['To'] = email
	
		
	try:
		s = smtplib.SMTP('smtpgw.futurice.com')
		s.sendmail(from_addr, email, msg.as_string())
		s.quit()
	except:
		return HttpResponse('EMAILFAIL')
	
	return HttpResponse('DONE')
	

