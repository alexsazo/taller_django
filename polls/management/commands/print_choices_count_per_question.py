from django.core.management.base import BaseCommand, CommandError
from polls.models import Question

class Command(BaseCommand):
    help = """
    Print count of choices per question saved in DB.
    """
    
    def add_arguments(self, parser):
        parser.add_argument('pk', nargs=1, type=int)
        
    def handle(self, *args, **options):
        "hago algo"
        pk = options['pk'][0]
        obj = Question.objects.get(id=pk)
        count = obj.choice_set.count()
        print("Tienes un total de {} alternativas en la base de datos para la pregunta {}".format(count,obj))
        
