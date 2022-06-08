from django import template
from django.contrib.auth.models import Group 

register = template.Library() 

#tag per il check nel template del nome dell'utente loggato
@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

#tag per trasformare valore in input in intero, usato sempre nel template
@register.filter()
def to_int(value):
    return int(value)