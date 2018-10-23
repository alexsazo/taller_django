from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from polls.models import Choice, Question

@login_required(login_url="/admin/")
def index(request):
    return render(request, 'polls/index.html', {})

def question_detail(request, question_pk):
    question = Question.objects.get(pk=question_pk)
    return render(request, 'polls/question_detail.html', {'question_para_template':question})
