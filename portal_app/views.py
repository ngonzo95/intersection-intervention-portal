from django.shortcuts import render, HttpResponse
from django.http import Http404
from .models import Intersection

# Create your views here.
def index(request):
    intersection_list = Intersection.objects.order_by("-number_of_accidents")[:20]
    context = {"intersection_list": intersection_list}
    return render(request, "portal_app/index.html", context)

def intersection_details(request, intersection_id):
    try:
        intersection = Intersection.objects.get(pk=intersection_id)
        print(intersection)
    except Intersection.DoesNotExist:
        raise Http404("Intersection does not exist")
    return render(request, "portal_app/intersection.html", {"intersection": intersection})

