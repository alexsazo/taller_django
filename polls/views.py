from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from polls.models import Choice, Question

from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.detail import DetailView, SingleObjectMixin

@login_required(login_url="/admin/")
def index(request):
    return render(request, 'polls/index.html', {})

def question_detail(request, question_pk):
    question = Question.objects.get(pk=question_pk)
    return render(request, 'polls/question_detail.html', {'question_para_template':question})


class QuestionDetailView(DetailView):
    context_object_name = "question_para_template"
    model = Question

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(*args, **kwargs)
        context['choices'] = self.object.choice_set.all()
        return context
