from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    # Root view
    (r'^$', 'futuUpload.views.index'),

    # Upload url
    (r'^(?P<folder>\d+)/$', 'futuUpload.views.upload'),
    
    #Zipping url
    (r'zip/(?P<folder>\d+)/$', 'futuUpload.views.zip'),
    
     # Get zip
    (r'^(?P<zip>\d+\.\w+)$', 'futuUpload.views.getzip'),
    
    #Send mail + sms
    (r'send/$', 'futuUpload.views.send'),
    
)
