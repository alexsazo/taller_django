from django.core.management.base import BaseCommand, CommandError
from polls.models import Question

class Command(BaseCommand):
    help = """
    Print count of Questions in DB.
    """
    
    # def add_arguments(self, parser):
    #     parser.add_argument('pk', nargs=1, type=int)
        
    def handle(self, *args, **options):
        "hago algo"
        count = Question.objects.count()
        print("Tienes un total de {} preguntas en la base de datos.".format(count))
        
