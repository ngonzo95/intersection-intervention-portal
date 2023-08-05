# inspired by this tutorial https://www.bugbytes.io/posts/django-unicorn-an-introduction/
from django_unicorn.components import UnicornView
from portal_app.models import Intersection

class IntersectionView(UnicornView):
    intersection_type = ""

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.intersection = Intersection.objects.get(pk=kwargs.get("intersection_id"))
        self.intersection_type = self.intersection.intersection_type

    def update_intersection_type(self):
        """ updates the intersection type """
        self.intersection.intersection_type = self.intersection_type
        self.intersection.save()
        # Movie.objects.create(name=self.name)
