from django.shortcuts import render
from django.http import HttpResponse
from .models import People

def display(request):
    try:
        people = People.objects.filter(homeworld__climate__icontains='windy').order_by('name')
        
        if not people.exists():
            raise Exception("No data")
            
        return render(request, 'ex09/display.html', {'people': people})
    except Exception:
        return HttpResponse("No data available, please use the following command line before use:<br>python manage.py loaddata ex09/ex09_initial_data.json")
