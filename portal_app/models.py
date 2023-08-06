from django.db import models

# Create your models here.
class Intersection(models.Model):
    lat = models.DecimalField(db_index=True, max_digits=20, decimal_places=16)
    lon = models.DecimalField(db_index=True, max_digits=20, decimal_places=16)
    intersection_type = models.CharField(db_index=True, max_length=80) 
    number_of_accidents = models.IntegerField(db_index=True)
    fatal_accident_number = models.IntegerField(db_index=True)
    major_accident_number = models.IntegerField(db_index=True) 
    minor_accident_number = models.IntegerField()  
    unknown_accident_number = models.IntegerField() 
    property_accident_number = models.IntegerField()
    average_cost_to_insurers = models.IntegerField()

    @property
    def intervention_count(self):
        return self.intervention_set.all().count()

    @property
    def formatted_cost_to_insurers(self):
        return  '${:0,.2f}'.format(self.average_cost_to_insurers)

class Intervention(models.Model):
    new_intersection_type = models.CharField(db_index=True, max_length=80)
    conversion_cost = models.DecimalField(db_index=True, max_digits=20, decimal_places=2) 
    accident_reduction_rate = models.DecimalField(max_digits=10, decimal_places=8) 
    accident_severity_reduction_rate = models.DecimalField(max_digits=10, decimal_places=8) 
    intersection = models.ForeignKey(
        "Intersection",
        on_delete=models.CASCADE,
    )

    @property
    def formatted_conversion_cost(self):
        return  '${:0,.2f}'.format(self.conversion_cost)
