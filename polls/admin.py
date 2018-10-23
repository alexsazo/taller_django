from django.contrib import admin

from polls.models import Question, Choice

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'question', 'choice_text', 'votes')
    list_filter = ('question',)
    readonly_fields = ('votes',)
    search_fields = ['question__question_text', 'choice_text']
    
