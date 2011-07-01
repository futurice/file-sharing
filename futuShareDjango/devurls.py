from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = patterns('',

    # Root view
    (r'^$', 'futuUpload.views.index'),

    # Upload url
    (r'^futushare/(?P<folder>\d+)/$', 'futuUpload.views.upload'),
    
    #Zipping url
    (r'futushare/zip/(?P<folder>\d+)/$', 'futuUpload.views.zip'),
    
     # Get zip
    (r'^(?P<zip>\d+\.\w+)$', 'futuUpload.views.getzip'),
    
    #Send mail + sms
    (r'futushare/send/$', 'futuUpload.views.send'),
    
)


urlpatterns += staticfiles_urlpatterns()
