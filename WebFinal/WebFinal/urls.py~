from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

   url(r'^admin/', include(admin.site.urls)),
   url(r'^todas/$', 'myapp.views.allActivities'),
   url(r'^ayuda/$', 'myapp.views.getHelp'),
   url(r'^update/$', 'myapp.views.update'),
   url(r'^tempadd/$', 'myapp.views.tempadd'),
   url(r'^actividad/(\d+)', 'myapp.views.activity'),
   url(r'^accounts/auth/', 'myapp.views.auth_view'),
   url(r'^preferencias/', 'myapp.views.preferencias'),
   #url(r'^accounts/loggedin/$', 'myapp.views.loggedin'),
   #url(r'^accounts/invalid/$', 'myapp.views.invalid_login'),
   #url(r'^admin/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login/'}),
   url(r'^css/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_URL2}),
   url(r'^logout/$', 'myapp.views.logout'),   
   url(r'^login/', 'myapp.views.login'),
   url(r'^prueba/', 'myapp.views.prueba'),
   url(r'^favicon.ico', 'myapp.views.user'),    
   url(r'^$', "myapp.views.index"),
   url(r'^(.*)/RSS', 'myapp.views.RSS'),  
   url(r'^(.*)', 'myapp.views.user'),	
     
  

)
