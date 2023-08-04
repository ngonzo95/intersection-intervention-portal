from django.shortcuts import render, HttpResponse
from .models import Intersection

# Create your views here.
def index(request):
    intersection_list = Intersection.objects.order_by("-number_of_accidents")[:20]
    context = {"intersection_list": intersection_list}
    return render(request, "portal_app/index.html", context)

def intersection_details(request, intersection_id):
    return HttpResponse("You're looking at question %s." % intersection_id)

