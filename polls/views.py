from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from polls.models import Choice, Question

from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.detail import DetailView, SingleObjectMixin

@login_required
def index(request):
    #DEVUELVE EL ESTADO DE AUTENTIFICACIÓN
    
    print("Usuario identificado?", request.user.is_authenticated())
    print(request.GET)
    
    if "state" not in request.session.keys():
        #GUARDA UNA VARIABLE ASOCIADA A LA SESIÓN
        request.session["state"] = 0
    elif request.GET.get('action') == '1':
        request.session["state"] += 1
    elif request.GET.get('action') == '0':
        request.session["state"] -= 1

    print(request.session["state"])
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


class QuestionListView(ListView):
    model = Question

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionListView, self).get_context_data(*args, **kwargs)
        context['diccionario'] = {"arg1":1, "arg2":2, "arg3":3}
        return context

class QuestionCreateView(CreateView):
    model = Question
    fields = ['question_text']


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['question_text']
    

def sessions_test(request):
    return render(request, 'polls/session_test.html', {})
