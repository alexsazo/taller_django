from django.conf.urls import url
from polls import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sessions_test/$', views.sessions_test, name='sessions_test'),
#    url(r'^question/(?P<question_pk>\d+)/$', views.question_detail, name='question-detail')
    url(r'^question/(?P<pk>\d+)/$', views.QuestionDetailView.as_view(), name='question-detail'),
    url(r'^question/(?P<pk>\d+)/edit/$', views.QuestionUpdateView.as_view(), name='question-update'),    
    url(r'^question/$', views.QuestionListView.as_view(), name='question-list'),
    url(r'^question/create/$', views.QuestionCreateView.as_view(), name='question-create'),
]
