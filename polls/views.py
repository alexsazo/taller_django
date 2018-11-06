from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from polls.models import Choice, Question

from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.detail import DetailView, SingleObjectMixin

from polls.forms import SimpleForm
from polls.forms import ChoiceForm
from polls.forms import ChoiceFormSet
from django.forms import formset_factory

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


class ChoiceCreateView(CreateView):
    model = Choice
    form_class = ChoiceForm
    template_name = 'polls/show_form.html'

    def get_form(self):
        #super(ChoiceCreateView, self).get_form()
        if self.request.method == 'GET':
            form = self.form_class(self.request.user)
        elif self.request.method == 'POST':
            form = self.form_class(self.request.user, self.request.POST)
        return form

def sessions_test(request):
    return render(request, 'polls/session_test.html', {})


def show_form(request):
    from django.db.models import Q
    condicion1 = Q(id__in=[2,4,5])
    condicion2 = Q(user=request.user)
    queryset_personalizada = Question.objects.filter(Q(condicion1 | condicion2))
    
    if request.method == "GET":
        form = SimpleForm(queryset_personalizada)
        
    elif request.method == "POST":
        form = SimpleForm(queryset_personalizada, request.POST)
        
        if form.is_valid():
            print("Es un formulario valido!")
            print(form.cleaned_data)
        else:
            print("Es invalido :(")


    return render(request, 'polls/show_form.html', {'form': form})

def show_model_form(request):
    
    if request.method == "GET":
        form = ChoiceForm(request.user)
        
    elif request.method == "POST":
        form = ChoiceForm(request.user, request.POST)
        
        if form.is_valid():
            print("Es un formulario valido!")
            print(form.cleaned_data)
            form.instance.save()
        else:
            print("Es invalido :(")


    return render(request, 'polls/show_form.html', {'form': form})


def show_formset(request):
    choiceform_factory = formset_factory(ChoiceForm, formset=ChoiceFormSet, min_num=10)
    
    if request.method == "GET":
        form = choiceform_factory(user=request.user)        
        
    elif request.method == "POST":
        form = choiceform_factory(request.POST, user=request.user)
        
        if form.is_valid():
           print("Es un formulario valido!")
           print(form.cleaned_data)
           form.instance.save()
        else:
            print("Es invalido :(")


    return render(request, 'polls/show_form.html', {'form': form})



# FORMSET USAGE EXAMPLE
    # def get_form(self):
    #     m = self.object.get_metadata()
    #     required_columns  = REQUIRED_COLUMNS_PER_EVALUATION[self.evaluation]
    #     initial = [{'key':key, 'required':required} for key, required in required_columns]
    #     initial2 = []
    #     for dic in initial:
    #         conf = m.get('config', {})
    #         evconf = conf.get(self.evaluation, {})
    #         colsconf = evconf.get('columns_config', {})
    #         column = colsconf.get(dic['key'])
    #         if column != None:
    #             dic['column'] = column
    #         initial2.append(dic)
            
    #     ff = formset_factory(form=self.formset_base_class,
    #                          formset=self.get_form_class(),
    #                          max_num=len(required_columns),
    #                          min_num=len(required_columns))
    #     args = []
    #     if self.request.method == "POST":
    #         args = [self.request.POST]
        
    #     fs = ff(*args, initial=initial2,
    #             evaluation=self.evaluation,
    #             sheet_name=self.selected_sheet_name,
    #             survey_upload=self.object)
    #     return fs

