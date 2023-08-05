from django.shortcuts import render, HttpResponse
from django.http import Http404
from .models import Intersection
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, ranges, LabelSet


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

    bar_source = ColumnDataSource(dict(x=["fatal", "major", "minor", "unknown", "property"],
    y=[intersection.fatal_accident_number, intersection.major_accident_number, intersection.minor_accident_number, 
    intersection.unknown_accident_number, intersection.property_accident_number]))

    x_label = "Accident Severity"
    y_label = "Number of Accidents"

    p_bar = figure(x_range=bar_source.data["x"], aspect_ratio=4, title="Intersection Accident Severity",
               toolbar_location=None, tools="", x_axis_label=x_label, y_axis_label=y_label, y_range= ranges.Range1d(start=0,end=1.1 * max(bar_source.data["y"])))

    p_bar.vbar(x="x", top="y", width=0.9, source=bar_source)

    p_bar.xgrid.grid_line_color = None

    labels = LabelSet(x='x', y='y', text='y', level='glyph',
                  text_align='center', y_offset=5, source=bar_source)

    p_bar.add_layout(labels)
 
    script, div = components(p_bar)

    return render(request, "portal_app/intersection.html", {"intersection": intersection, "script": script, "div": div})

