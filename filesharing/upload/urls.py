import views

urlpatterns = ('upload.views',
   # Root view
    (r'^$', 'index'),

    # Upload url
    (r'^(?P<folder>\d+)/$', 'upload'),
    
    #Zipping url
    (r'zip/(?P<folder>\d+)/$', 'zip'),
    
     # Get zip
    (r'^(?P<zip>\d+\.\w+)$', 'getzip'),
    
    #Send mail + sms
    (r'send/(?P<file>\d+\..+)/(?P<email>.+)/(?P<phone>.+)/(?P<password>.+)/$', 'send'),
    
)

