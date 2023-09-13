from django.core.management.base import BaseCommand
import csv
from decimal import Decimal
from ...models import Intersection
from ...models import Intervention

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    #logger.info("Delete All itersections and interventions")
    Intervention.objects.all().delete()
    Intersection.objects.all().delete()


def create_intersection(intersection_data):
    """Creates an intersection"""
    #logger.info("Creating intersection from csv")
    row = intersection_data
    print(row.keys())

    intersection = Intersection(
        lat= Decimal(row["lat"]),
        lon= Decimal(row["lon"]),
        cluster_id= row["cluster_id"],
        intersection_type= row["intersection_type"],
        number_of_accidents= row["number_of_accidents"],
        average_cost_to_insurers= Decimal(row["average_cost_to_insurers"]),
    )
    intersection.save()
    #logger.info("{} intersection created.".format(intersection))
    return intersection

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Load form csv
    with open('portal_app/portal_app_sioux_and_davenport.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            else:
                print(f'\t{row["lat"]} \t{row["lon"]}  being proccessed.')
                create_intersection(row)
            line_count += 1
        print(f'Processed {line_count} lines.')

