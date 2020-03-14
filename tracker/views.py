
from django.http import HttpResponseBadRequest, JsonResponse

from django.shortcuts import render
from .models import Number

import json


def index(request):
    return render(request, 'tracker/index.html')


def track_or_increment_number_helper(request, number_to_track, increment_by):

    if Number.objects.filter(value=number_to_track):
        number = Number.objects.get(value=number_to_track)
        if increment_by:
            number.incrementCount(increment_by)
        else:
            number.incrementCount(1)
        number.save()

        if request.content_type == 'application/json':
            response = {'number': str(number.value), 'count': str(number.count)}
            return JsonResponse(response, content_type='application/json')
        else:
            return render(request, 'tracker/track_or_increment.html', {'number': number})

    else:
        if increment_by:
            return HttpResponseBadRequest("Cannot increment a number that has not been tracked before")
        else:
            added_number = Number.objects.create(value=number_to_track)
            added_number.save()

            if request.content_type == 'application/json':
                response = {'number': str(added_number.value), 'count': str(added_number.count)}
                return JsonResponse(response, content_type='application/json')
            else:
                return render(request, 'tracker/track_or_increment.html', {'number': added_number})


def get_request_attribute(request, attribute):
    if request.content_type == "application/json":
        body = json.loads(request.body.decode("utf-8"))
        return body.get(attribute)
    elif request.content_type == "application/x-www-form-urlencoded" or request.content_type == "text/plain":
        if request.method == "POST":
            return request.POST.get(attribute)
        elif request.method == "PUT":
            return request.PUT.get(attribute)
        ### To handle cases when responses are sent through an html form,
        ### since html forms do not support PUT as a method type, it's sent as a GET request instead
        elif request.method == "GET":
            return request.GET.get(attribute)


def track_or_increment(request):
    number_to_track = get_request_attribute(request, "number")
    increment_by = get_request_attribute(request, "increment_value")

    if increment_by is not None:
        increment_by = int(increment_by)
        if increment_by < 1:
            return HttpResponseBadRequest("Increment amount must be greater than zero")

    if number_to_track:
        return track_or_increment_number_helper(request, number_to_track, increment_by)
    else:
        return HttpResponseBadRequest("Request is missing number attribute")


def get_all_numbers(request):
    all_numbers = Number.objects.all()
    if request.content_type == "application/json":
        numbers_array = []
        for number in all_numbers:
            numbers_array.append({'number': number.value, 'count': number.count})
        response = {'all_numbers': numbers_array}

        return JsonResponse(response, content_type="application/json")
    else:
        return render(request, 'tracker/get_all_numbers.html', {'all_numbers': all_numbers})


def delete(request, number):
    number_to_delete = Number.objects.filter(value=number)

    if number_to_delete:
       number_to_delete.delete()
       if request.content_type == "application/json":
           return JsonResponse({'message': f"Deleted number {number}"}, content_type="application/json")
       else:
            return render(request, 'tracker/delete.html', {'number': number})
    else:
        return HttpResponseBadRequest(f"Cannot delete the number {number}, it has not been tracked yet")
