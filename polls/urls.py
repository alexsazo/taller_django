from django.conf.urls import url
from polls import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^question/(?P<question_pk>\d+)/$', views.question_detail, name='question-detail')    
]
