from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.
def home(request):
    date = datetime.datetime.now()
    h = int(date.strftime('%H'))
    
    msg ='Good'
    
    if h < 12:
        msg += 'Morning'
        
    elif h < 16:
        msg += 'Afternoon'
        
    elif h < 18:
        msg += 'Evening'
        
    else:
        msg += 'Night'
        
        
    greeting = f'{msg}! Nkemstrong' 
    
    tasks = [
        {'id': 1, 'text': 'Cook breakfast', 'done': True},
        {'id': 2, 'text': 'Wash dishes', 'done': False},
        {'id': 3, 'text': 'Clean the house', 'done': False},
        {'id': 4, 'text': 'Do laundry', 'done': False},
        {'id': 5, 'text': 'Netflix and Chills', 'done': False}
    ]
    
    context = {
        'greeting': greeting,
        'tasks': tasks
    }
    
    
    return render(request, 'home.html', context)

        
def login(request):
    return render(request, 'login.html')


# username = 'Nkemstrong'
#     context = {
#         'username':username
#     }
    