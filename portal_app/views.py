from django.shortcuts import render, HttpResponse
from django.http import Http404
from .models import Intersection
from bokeh.plotting import figure, gmap
from bokeh.embed import components
from bokeh.models import ColumnDataSource, ranges, LabelSet, GMapOptions, LinearColorMapper, HoverTool, TapTool, OpenURL
from django.urls import reverse



"""
This route handles the index page which shows a list of all intersections 
"""
def index(request):
    intersection_list = Intersection.objects.order_by("-number_of_accidents")[:20]
    
    map_options = GMapOptions(lat=42.511975, lng=-94.167375, map_type="roadmap", zoom=7)
    p = gmap("AIzaSyBrYytD5OWJtME3ydbBiFfJ8pSnhdQNa3Q", map_options, title="Iowa Collisions", tools=["pan","wheel_zoom"], height_policy="max", width_policy="max")

    source = ColumnDataSource(
        data={
            "number_of_accidents": [x.number_of_accidents for x in intersection_list],
            "cost_to_insures": [x.average_cost_to_insurers for x in intersection_list],
            "lats": [float(x.lat) for x in intersection_list],
            "lons": [float(x.lon) for x in intersection_list],
            "ids" : [x.id for x in intersection_list]

        }
    )

    p.circle(x="lons", y="lats", size=12,  source=source)

    TOOLTIPS = [
        ("Total # of Accidents", "@number_of_accidents{0,0}"),
        ("Average Yearly cost to Insurers","$@cost_to_insures{0,0}")
    ]
    p.add_tools( HoverTool(tooltips=TOOLTIPS))
    map_script, map_div = components(p)

    url = request.get_host() + "/intersections/@ids"
    print(url)

    p.add_tools(TapTool(callback = OpenURL(url=url)))

    return render(request, "portal_app/index.html", {"intersection_list": intersection_list, "map_script": map_script, "map_div": map_div})




"""
This route handles the page for a particular intersection.
"""
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
               toolbar_location=None, tools="", x_axis_label=x_label, y_axis_label=y_label, y_range= ranges.Range1d(start=0,end=1.3 * max(bar_source.data["y"])), height_policy="max", width_policy="max")

    p_bar.vbar(x="x", top="y", width=0.9, source=bar_source)

    p_bar.xgrid.grid_line_color = None

    labels = LabelSet(x='x', y='y', text='y', level='glyph',
                  text_align='center', y_offset=5, source=bar_source)

    p_bar.add_layout(labels)
 
    script, div = components(p_bar)

    return render(request, "portal_app/intersection.html", {"intersection": intersection, "script": script, "div": div})

