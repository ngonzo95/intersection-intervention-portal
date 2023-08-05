from django_unicorn.components import UnicornView
from portal_app.models import Intervention


class InterventionView(UnicornView):
    conversion_cost = 0
    new_intersection_type = ""
    accident_reduction_rate = 0
    acccident_severity_reduction_rate = 0

    interventions = Intervention.objects.none()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.intersection_id = kwargs.get("intersection_id")
        self.interventions = Intervention.objects.all().filter(intersection_id=self.intersection_id)

    def add_intervention(self):
        """ Create a new intervention and clear all of the other fields """
        Intervention.objects.create(conversion_cost=self.conversion_cost, 
            new_intersection_type=self.new_intersection_type, 
            accident_reduction_rate=self.accident_reduction_rate,
            accident_severity_reduction_rate=self.acccident_severity_reduction_rate,
            intersection_id=self.intersection_id
        )
        self.interventions = Intervention.objects.all().filter(intersection_id=self.intersection_id)
        
        self.conversion_cost = 0
        self.new_intersection_type = ""
        self.accident_reduction_rate = 0
        self.acccident_severity_reduction_rate = 0

    def delete_intervention(self, intervention_id):
        Intervention.objects.filter(pk=intervention_id).delete()
        self.interventions = Intervention.objects.all().filter(intersection_id=self.intersection_id)

