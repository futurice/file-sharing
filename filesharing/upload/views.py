from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from os import path, makedirs, listdir
from upload.forms import PasswordForm
from upload.models import Zip
import smtplib
import subprocess, random, string, urllib2, re, shutil, mimetypes, time

# Renders the frontpage
def index(request):
    return render_to_response('upload/index.html')


# This method saves a file posted to it in the directory specified in the settings
def upload(request, folder):
    if request.method == 'POST':
        for field_name in request.FILES:
            uploaded_file = request.FILES[field_name]

            if uploaded_file.size > settings.MAX_UPLOAD_FILE_SIZE:
                return HttpResponse('File was too big.')

            # Create folder
            dir = settings.UPLOAD_DIRECTORY + folder + '/'
            if not path.exists(dir):
                try:
                    makedirs(dir)
                except:
                    time.sleep(1)
                    if not path.exists(dir):
                        print 'Temporary path could not be created.'
                        return HttpResponseServerError

            # Save to folder
            destination_path = dir + uploaded_file.name
            destination = open(destination_path, 'wb+')
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
            destination.close()
        return HttpResponse('DONE')
    else:
        return HttpResponseNotFound()

def getzip(request, zip_file):
    """ Redirect the user to the address specified in ZIP_URL
        This is used for old password protected zip files """
    return HttpResponseRedirect(settings.ZIP_URL + zip_file)


def zip_files(request, folder):
    """ Zip the files in the folder specified in the arguments and save
        the zip to the path defined in the settings """

    if request.method == 'POST':
        password_length = settings.PASSWORD_LENGTH

        # Hard to remember password
        #password = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))

        # Easier to remember password
        proc = subprocess.Popen(["pwgen", str(password_length), "1"], stdout=subprocess.PIPE)
        (password, _) = proc.communicate()
        password = password.strip()

        # Generate list of files
        try:
            files = []
            for filename in listdir(settings.UPLOAD_DIRECTORY + folder + '/'):
                files.append(settings.UPLOAD_DIRECTORY + folder + '/' + filename)
        except IOError:
            return HttpResponseRedirect('/')

        #Path for the zip
        zippath = settings.FREE_ZIP_DIR + folder + '.zip'

        #Check for a zip with the same name so we can't add to existing zips
        if path.exists(zippath):
            print 'Tried to add to existing zip file'
            return HttpResponseServerError()


        #Zip it! using 7zip
        #arguments = ['/usr/bin/7z', 'a', '-p'+password, '-y', zippath] + files
        #zip7z = subprocess.call(arguments)

        #Zip it! using zip
        arguments = ['/usr/bin/zip', '-j', '-y', zippath] + files
        zip7z = subprocess.call(arguments)

        #Remove the individual files
        shutil.rmtree(settings.UPLOAD_DIRECTORY + folder + '/')

        #Was the zipping successful?
        if not zip7z:
            pw_zip = Zip(filename=folder+'.zip', password=password)
            pw_zip.save()

            return render_to_response('upload/done.html', {'file': folder + '.zip',
                     'password': password, 'link': settings.SERVER_ROOT_ADDRESS + 'ask/' + folder + '.zip'})

        else:
            print 'Something went wrong while trying to zip the files. Make sure zip is installed and working.'
            print 'zip exit code: %d' % zip7z
            print " ".join(arguments)

            return HttpResponseServerError()

    else:
        #If you try something other than POST, you are redirected to the front page
        return HttpResponseRedirect('/')


def send(request):
    """ Send an email and an sms to the specified addresses """

    if request.method == 'POST':
        post = request.POST

        #Get the variables from the post
        email = post.__getitem__('email')
        phone = post.__getitem__('phone')
        password = post.__getitem__('password')
        filename = post.__getitem__('file')

        #Validate mail and phone
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponse('BADEMAIL')

        if settings.SMS:
            if re.match(r"00(\d+)$", phone) == None:
                return HttpResponse('BADPHONE')

        #Send SMS
        sms = urllib2.quote(render_to_string('mails/file_sms.txt', {'password' : password}))

        smsurl = settings.SMS_BASE_URL%(phone, sms)

        if settings.SMS:
            response = urllib2.urlopen(settings.SMS_URL)
            html = response.read()
            if html != '0: Accepted for delivery': #Kannel response body
                return HttpResponse('SMSFAIL')

        #Send Email
        email_body = render_to_string('mails/file_email.txt', {'url': '%sask/%s'%(settings.SERVER_ROOT_ADDRESS, filename)})

        try:
            send_mail(settings.EMAIL_SUBJECT, email_body, settings.EMAIL_FROM, [email], fail_silently=False)
        except smtplib.SMTPException:
            return HttpResponse('EMAILFAIL')

        return HttpResponse('DONE')
    else:
        return HttpResponseNotFound()


def password_check(request, requested_filename):

    # Check if we're posting the password
    if request.method == 'POST':
        form = PasswordForm(request.POST)

        if form.is_valid():

            #Get the variables from the post
            password = form.cleaned_data['password']
            requested_filename = form.cleaned_data['filename']

            # If there's no such file, return 404
            f = get_object_or_404(Zip, filename=requested_filename)

            # Is the password correct?
            if f.is_correct(password):

                # Serve file
                mimetypes.init()
                try:
                    file_path = settings.FREE_ZIP_DIR + '/' + requested_filename
                    file_socket = open(file_path, "r")
                    filename = path.basename(file_path)
                    mime_type_guess = mimetypes.guess_type(filename)

                    if mime_type_guess is not None:
                        response = HttpResponse(file_socket, mimetype=mime_type_guess[0])
                        response['Content-Disposition'] = 'attachment; filename=' + filename

                except IOError:
                    return render_to_response('upload/ask.html', {'form': form, 'status' : 'There was an error reading the file.'}, context_instance=RequestContext(request))

                return response

            else:
                return render_to_response('upload/ask.html', {'form': form, 'status' : 'Wrong password.'}, context_instance=RequestContext(request))
        else:
            return render_to_response('upload/ask.html', {'form': form}, context_instance=RequestContext(request))

    else:
        # If we're not posting, the password prompt page is shown
        get_object_or_404(Zip, filename=requested_filename)
        form = PasswordForm(initial={'filename': requested_filename})
        return render_to_response('upload/ask.html', {'form': form}, context_instance=RequestContext(request))
