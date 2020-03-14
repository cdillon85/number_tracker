from django.http import HttpResponse, HttpResponseBadRequest

from django.shortcuts import render
from .models import Number


def index(request):
    return render(request, 'tracker/index.html')


def track_or_increment_number(request, number_to_track, increment_by):

    if Number.objects.filter(value=number_to_track):
        number = Number.objects.get(value=number_to_track)
        if increment_by:
            number.incrementCount(increment_by)
        else:
            number.incrementCount(1)
        number.save()
        return render(request, 'tracker/track_or_increment.html', {'number': number})

    else:
        if increment_by:
            return HttpResponseBadRequest("Cannot increment a number that has not been tracked before")
        else:
            added_number = Number.objects.create(value=number_to_track)
            added_number.save()
            return render(request, 'tracker/track_or_increment.html', {'number': added_number})


def track_or_increment(request):
    number_to_track = None
    increment_by = None

    if request.method == "POST":
        number_to_track = request.POST.get('number')
    elif request.method == "PUT":
        number_to_track = request.PUT.get('number')
        increment_by = request.PUT.get('increment_value')

    ### To handle cases when responses are sent through an html form,
    ### since html forms do not support PUT as a method type, it's sent as a GET request instead
    elif request.method == "GET":
        number_to_track = request.GET.get('number')
        increment_by = int(request.GET.get('increment_value'))

    if increment_by is not None and increment_by < 1:
        return HttpResponseBadRequest("Increment amount must be greater than zero")

    if number_to_track:
        return track_or_increment_number(request, number_to_track, increment_by)
    else:
        return HttpResponseBadRequest("Request is missing number attribute")


def get_all_numbers(request):
    all_numbers = Number.objects.all()
    return render(request, 'tracker/get_all_numbers.html', {'all_numbers': all_numbers})


def delete(request, number):
    Number.objects.filter(value=number).delete()
    return render(request, 'tracker/delete.html', {'number': number})
