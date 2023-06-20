from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.shortcuts import render

from django.contrib.auth.models import User
from .models import *


def chat(request):
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)


def user_stats(request):
    users = User.objects.all()
    user_stats = UserStats.objects.select_related('user')

    return render(request, 'chatbot_tutorial/user_stats.html', {'users': users, 'user_stats': user_stats})


def respond_to_websockets(message):
    jokes = {
     'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
     'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
     'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] 
     }  

    result_message = {
        'type': 'text'
    }
    if 'dumb' in message['text'] or 'fat' in message['text'] or 'stupid' in message['text']:
        # Increment the count for the selected button
        button_stats, _ = ButtonStats.objects.get_or_create(user_id=message['user_id'], button=message['text'])
        button_stats.count += 1
        button_stats.save()

        # Increment the count for the corresponding user
        user_stats, _ = UserStats.objects.get_or_create(user_id=message['user_id'])
        setattr(user_stats, message['text'].lower() + '_count', getattr(user_stats, message['text'].lower() + '_count') + 1)
        user_stats.save()

    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])
    
    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])
    
    elif 'dumb' in message['text']:
        result_message['text'] = random.choice(jokes['dumb'])

    elif message['text'] in ['hi', 'hey', 'hello']:
        result_message['text'] = "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."

    return result_message



    