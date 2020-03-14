from django.http import HttpResponse

from django.shortcuts import render

def index(request):
    return render(request, 'tracker/index.html')

def track_or_increment_number(request):
    return HttpResponse("Add or update a number.")

def get_all_numbers(request):
    return HttpResponse("Here's all the numbers you have tracked so far.")

def delete(request, number):
    return HttpResponse(f"You deleted the number {number}")