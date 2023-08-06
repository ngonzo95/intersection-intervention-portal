# inspired by this tutorial https://www.bugbytes.io/posts/django-unicorn-an-introduction/
from django_unicorn.components import UnicornView
from portal_app.models import Intersection
from django.urls import reverse


class IntersectionView(UnicornView):
    intersection_type = ""
    next_path = ""
    prev_path= ""

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.intersection = Intersection.objects.get(pk=kwargs.get("intersection_id"))
        self.intersection_type = self.intersection.intersection_type
        self.next_path = self._next_intersection_path()
        self.prev_path = self._prev_intersection_path()

    def update_intersection_type(self):
        """ updates the intersection type """
        self.intersection.intersection_type = self.intersection_type
        self.intersection.save()
    
    def _prev_intersection_path(self):
        inter = Intersection.objects.raw("select pai.* from portal_app_intersection pai where pai.average_cost_to_insurers  > (select pai2.average_cost_to_insurers from portal_app_intersection pai2 where pai2.id = %s) order by pai.average_cost_to_insurers limit 1", [self.intersection.id])[0]
        return reverse("intersections", args=[inter.id])

    def _next_intersection_path(self):
        inter = Intersection.objects.raw("select pai.* from portal_app_intersection pai where pai.average_cost_to_insurers  < (select pai2.average_cost_to_insurers from portal_app_intersection pai2 where pai2.id = %s) order by  pai.average_cost_to_insurers  desc limit 1", [self.intersection.id])[0]
        return reverse("intersections", args=[inter.id])
