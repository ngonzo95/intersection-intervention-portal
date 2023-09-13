from django.db import models
from decimal import Decimal
from datetime import datetime

# Create your models here.
class Intersection(models.Model):
    lat: Decimal = models.DecimalField(db_index=True, max_digits=20, decimal_places=16)
    lon: Decimal = models.DecimalField(db_index=True, max_digits=20, decimal_places=16)
    cluster_id: int = models.IntegerField() 
    intersection_type: str = models.CharField(db_index=True, max_length=80) 
    number_of_accidents: int = models.IntegerField(db_index=True)
    average_cost_to_insurers: int = models.IntegerField()

    @property
    def intervention_count(self):
        return self.intervention_set.all().count()

    @property
    def formatted_cost_to_insurers(self): 
        if type(self.average_cost_to_insurers) == str:
            return '${:0,.2f}'.format(Decimal(self.average_cost_to_insurers))
        else:
            return  '${:0,.2f}'.format(self.average_cost_to_insurers)

class Intervention(models.Model):
    new_intersection_type: str = models.CharField(db_index=True, max_length=80)
    conversion_cost: Decimal  = models.DecimalField(db_index=True, max_digits=20, decimal_places=2) 
    accident_reduction_rate: Decimal  = models.DecimalField(max_digits=10, decimal_places=8) 
    accident_severity_reduction_rate: Decimal  = models.DecimalField(max_digits=10, decimal_places=8) 
    intersection = models.ForeignKey(
        "Intersection",
        on_delete=models.CASCADE,
    )

    @property
    def formatted_conversion_cost(self):
        if type(self.conversion_cost) == str:
            return '${:0,.2f}'.format(Decimal(self.conversion_cost))
        else:
            return  '${:0,.2f}'.format(self.conversion_cost)

class Accident(models.Model):
    accident_index: int = models.IntegerField()
    x: Decimal = models.DecimalField(db_index=True, max_digits=20, decimal_places=16)
    y: Decimal = models.DecimalField(db_index=True, max_digits=20, decimal_places=16)
    charged_num: int = models.IntegerField(null=True,)
    bac: Decimal  = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    was_drug_tested_num: int = models.IntegerField(null=True)
    drug_test_result_num: int = models.IntegerField(null=True)
    driver_condition_num: int = models.IntegerField(null=True)
    vision_obscured: int = models.IntegerField(null=True)
    contributing_circumstaces_1_num: int = models.IntegerField(null=True)
    contributing_circumstaces_2_num: int = models.IntegerField(null=True)
    vehicle_type_num: int = models.IntegerField(null=True)
    vehicle_year: int = models.IntegerField(null=True)
    vehicle_make: str = models.CharField(db_index=True, max_length=80, null=True) 
    vehicle_model: str = models.CharField(db_index=True, max_length=80, null=True) 
    occupants: int = models.IntegerField(null=True)
    vehicle_action_num: int = models.IntegerField(null=True)
    sequence_of_events_1_num: int = models.IntegerField(null=True)
    sequence_of_events_2_num: int = models.IntegerField(null=True)
    sequence_of_events_3_num: int = models.IntegerField(null=True)
    sequence_of_events_4_num: int = models.IntegerField(null=True)
    most_harmful_event_num: int = models.IntegerField(null=True)
    speed_limit: int = models.IntegerField(null=True)
    traffic_control_num: int = models.IntegerField(null=True)
    fixed_object_struck_num: int = models.IntegerField(null=True)
    most_damage_area_num: int = models.IntegerField(null=True)
    extent_of_damage_num: int = models.IntegerField(null=True)
    crash_severity: int = models.IntegerField(null=True)
    major_cause_num: int = models.IntegerField(null=True)
    surface_conditions_num: int = models.IntegerField(null=True)
    road_type_num: int = models.IntegerField(null=True)
    total_fatalities: int = models.IntegerField(null=True)
    crash_year: int = models.IntegerField(null=True)
    crash_datetime: datetime = models.DateTimeField(null=True, blank=True)
    cluster_id: int = models.IntegerField(null=True)
    intersection = models.ForeignKey(
        "Intersection",
        on_delete=models.CASCADE,
        null=True
    )


