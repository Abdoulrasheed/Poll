from django.conf.urls import url

from bitpoint.messenger import views

urlpatterns = [
    url(r'^$', views.inbox, name='inbox'),
    url(r'^send/$', views.send, name='send_message'),
    url(r'^new/$', views.new, name='new_message'),
    url(r'^check/$', views.check, name='check_message'),
    url(r'^users/$', views.users, name='users_message'),
    url(r'^delete/$', views.delete, name='delete_message'),
    url(r'^(?P<ID_Number>[^/]+)/$', views.messages, name='messages'),
]
