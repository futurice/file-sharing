from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Root view
    (r'^$', 'upload.views.index'),
    # Upload url
    (r'^(?P<folder>\d+)/$', 'upload.views.upload'),
    #Zipping url
    (r'zip/(?P<folder>\d+)/$', 'upload.views.zip_files'),
    # Get zip
    (r'^(?P<zip>\d+\.\w+)$', 'upload.views.getzip'),
    #Send mail + sms
    (r'send/$', 'upload.views.send'),
    # Password prompt
    (r'ask/(?P<requestedFilename>\d+\.\w+)$', 'upload.views.password_check'),
)
