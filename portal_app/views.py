from django.shortcuts import render
from django.http import Http404
from .models import Intersection, Accident
from bokeh.plotting import gmap
from bokeh.embed import components
from bokeh.models import ColumnDataSource, ranges, LabelSet, GMapOptions, HoverTool, TapTool, OpenURL
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bokeh.models import TabPanel, Tabs
from bokeh.plotting import figure
import pandas as pd
from math import pi
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from collections import defaultdict


"""
This route handles the index page which shows a list of all intersections 
"""
def index(request):
    intersection_list = Intersection.objects.order_by("-number_of_accidents").all()

    page = request.GET.get('page', 1)
    paginator = Paginator(intersection_list, 20)
    
    try:
        intersections = paginator.page(page)
    except PageNotAnInteger:
        intersections = paginator.page(1)
    except EmptyPage:
        intersections = paginator.page(paginator.num_pages)

    
    map_script, map_div = _generate_intersection_plot(intersections, request)

    return render(request, "portal_app/index.html", {"intersection_list": intersections, "map_script": map_script, "map_div": map_div})




"""
This route handles the page for a particular intersection.
"""
def intersection_details(request, intersection_id):
    try:
        intersection = Intersection.objects.get(pk=intersection_id)
        print(intersection)
    except Intersection.DoesNotExist:
        raise Http404("Intersection does not exist")

    accidents = Accident.objects.filter(intersection_id=intersection_id)
    script, div = _generate_accident_charts(accidents)

    return render(request, "portal_app/intersection.html", {"intersection": intersection, "script": script, "div": div, "prev_intersection_path": _prev_intersection_path(intersection), "next_intersection_path": _next_intersection_path(intersection)})

def _generate_accident_charts(accidents):
    accidents_df = pd.DataFrame(list(accidents.values("crash_severity", "crash_year", "contributing_circumstaces_1_num")))

    sev_bar = _generate_bar_graph(accidents_df, "crash_severity", label_dict=severity_dict, title="Severity",
                                x_label = "Accident Severity")
    year_bar = _generate_bar_graph(accidents_df, "crash_year", title="Crash Year", x_label = "Accident Year")
    most_harm_pie = _generate_pie_chart(accidents_df, "contributing_circumstaces_1_num", label_dict=dcontcirc_dict, title="Major harm")

    tab1 = TabPanel(child=sev_bar, title="Severity")
    tab2 = TabPanel(child=year_bar, title="Crash Year")
    tab3 = TabPanel(child=most_harm_pie, title= "Most Harm")
    return components(Tabs(height= 200, tabs=[tab1, tab2, tab3]))

def _generate_intersection_plot(intersection_list, request):
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

    url = "/intersections/@ids"
    p.add_tools(TapTool(callback = OpenURL(url=url)))
    return components(p)

def _prev_intersection_path(intersection):
        inter = Intersection.objects.raw("select pai.* from portal_app_intersection pai where pai.average_cost_to_insurers  > (select pai2.average_cost_to_insurers from portal_app_intersection pai2 where pai2.id = %s) order by pai.average_cost_to_insurers limit 1", [intersection.id])
        if len(inter) == 0:
            return None
        else:
            return reverse("intersections", args=[inter[0].id])

def _next_intersection_path(intersection):
    inter = Intersection.objects.raw("select pai.* from portal_app_intersection pai where pai.average_cost_to_insurers  < (select pai2.average_cost_to_insurers from portal_app_intersection pai2 where pai2.id = %s) order by  pai.average_cost_to_insurers  desc limit 1", [intersection.id])
    if len(inter) == 0:
        return None
    else:
        return reverse("intersections", args=[inter[0].id])


vaction_dict = { 1: "Movement essentially straight", 2: "Turning left", 3: "Turning right", 4: "Making U-turn", 5: "Overtaking/passing",
                 6: "Changing lanes", 7: "Entering traffic lane (merging)",8: "Leaving traffic lane", 9: "Backing", 10: "Slowing/stopping (deceleration)",
                 11: "Stopped in traffic", 12: "Legally Parked", 13: "Illegally Parked/Unattended", 14: "Negotiating a curve", 15: "Starting in road",
                 16: "Accelerating in road", 17: "Leaving a parked position", 18: "Entering a parked position", 98: "Other (explain in narrative)",
                 99: "Unknown", 77: "Not Reported" }

major_cause_dict = {1: "Animal", 2: "Ran Traffic Signal", 3: "Ran Stop Sign", 4: "Failed to yield to emergency vehicle",
                    5: "FTYROW:  At uncontrolled intersection", 6: "FTYROW:  Making right turn on red signal", 7: "FTYROW:  From stop sign", 8: "FTYROW:  From yield sign",
                    9: "FTYROW:  Making left turn", 10: "FTYROW:  From driveway", 11: "FTYROW:  From parked position", 12: "FTYROW:  To pedestrian", 13: "FTYROW:  Other (explain in narrative)",
                    14: "Drove around RR grade crossing gates", 15: "Disregarded RR Signal", 16: "Crossed centerline (undivided)", 17: "Crossed median (divided)",
                    18: "Traveling wrong way or on wrong side of road", 19: "Aggressive driving/road rage", 20: "Driving too fast for conditions", 21: "Exceeded authorized speed",
                    22: "Improper or erratic lane changing", 23: "Operating vehicle in an reckless, erratic, careless, negligent manner", 24: "Followed too close",
                    25: "Passing:  On wrong side", 26: "Passing:  Where prohibited by signs/markings", 27: "Passing:  With insufficient distance/inadequate visibility",
                    28: "Passing:  Through/around barrier", 29: "Passing:  Other passing (explain in narrative)", 30: "Made improper turn", 31: "Driver Distraction:  Manual operation of an electronic communication device",
                    32: "Driver Distraction:  Talking on a hand-held device", 33: "Driver Distraction:  Talking on a hands free device", 34: "Driver Distraction:  Adjusting devices (radio, climate)",
                    35: "Driver Distraction:  Other electronic device activity", 36: "Driver Distraction:  Passenger", 37: "Driver Distraction:  Unrestrained animal", 38: "Driver Distraction:  Reaching for object(s)/fallen object(s)",
                    39: "Driver Distraction:  Inattentive/lost in thought", 40: "Driver Distraction:  Other interior distraction", 41: "Driver Distraction:  Exterior distraction",
                    42: "Ran off road - right", 43: "Ran off road - straight", 44: "Ran off road - left", 45: "Lost Control", 46: "Swerving/Evasive Action", 47: "Over correcting/over steering",
                    48: "Failed to keep in proper lane", 49: "Failure to signal intentions", 50: "Traveling on prohibited traffic way", 51: "Vehicle stopped on railroad tracks", 52: "Other (explain in narrative):  Vision obstructed",
                    53: "Other (explain in narrative):  Improper operation", 54: "Other (explain in narrative):  Disregarded Warning Sign", 55: "Other (explain in narrative):  Disregarded signs/road markings",
                    56: "Other (explain in narrative):  Illegal off-road driving", 57: "Downhill runaway", 58: "Separation of units", 59: "Towing Improperly", 60: "Cargo/equipment loss or shift",
                    61: "Equipment failure", 62: "Oversized Load/Vehicle", 63: "Other (explain in narrative):  Getting off/out of vehicle", 64: "Failure to dim lights/have lights on",
                    65: "Improper Backing", 66: "Improper Starting", 67: "Illegally Parked/Unattended", 68: "Driving less than the posted speed limit", 69: "Operator inexperience",
                    70: "Other (explain in narrative):  Other", 71: "Unknown", 72: "Not Reported", 73: "Other (explain in narrative):  No improper action", 99: "None Indicated"
                    }

dcontcirc_dict = defaultdict(lambda: f"Unknown num", {
    1: "Ran traffic signal", 2: "Ran stop sign", 3: "Exceeded authorized speed", 4: "Driving less than the posted speed limit",
    5: "Driving too fast for conditions", 6: "Lost Control", 7: "Followed too close", 8: "Operating vehicle in an reckless, erratic, careless, negligent manner",
    9: "Improper or erratic lane changing", 10: "Aggressive driving/road rage", 11: "Made improper turn", 12: "Failed to yield to emergency vehicle",
    13: "Traveling wrong way/on wrong side", 14: "Traveling on prohibited traffic way", 15: "Over-correcting/over-steering", 16: "Failed to keep in proper lane",
    17: "Failure to signal intentions", 18: "Swerved to avoid: vehicle, object, non-motorist, or animal in roadway", 19: "Starting or backing improperly",
    20: "Failure to dim lights/have lights on", 21: "Vehicle stopped on railroad tracks", 22: "Vehicle drove around grade crossing gates", 30: "Passing:  On wrong side",
    31: "Passing:  Where prohibited by signs/markings", 32: "Passing:  With insufficient distance/inadequate visibility", 33: "Passing:  Through/around barrier",
    96: "Passing:  Other passing (explain in narrative)", 40: "FTYROW:  From stop sign", 41: "FTYROW:  From yield sign", 42: "FTYROW:  Making left turn",
    43: "FTYROW:  Making right turn on red signal", 44: "FTYROW:  From driveway", 45: "FTYROW:  From parked position", 46: "FTYROW:  To non-motorist", 47: "FTYROW:  At uncontrolled intersection",
    97: "FTYROW:  Other FTYROW (explain in narrative)", 50: "Other (explain in narrative):  Vision obstructed", 51: "Other (explain in narrative):  Operating without required equipment",
    52: "Other (explain in narrative):  Failure to obey displayed vehicle warnings or instructions", 53: "Other (explain in narrative):  Disregarded signs/road markings", 54: "Other (explain in narrative):  Illegal off-road driving",
    55: "Other (explain in narrative):  Towing improperly", 56: "Other (explain in narrative):  Getting off/out of vehicle", 57: "Other (explain in narrative):  Overloading/improper loading with passengers/cargo",
    58: "Operator inexperience", 88: "No improper action", 98: "Other (explain in narrative)", 99: "Unknown", 77: "Not Reported"
})

severity_dict = {1: "fatal", 2: "major", 3: "minor", 4: "unknown", 5: "property"}


def _generate_bar_graph(df, column_name, label_dict=None, title="", x_label="", y_label= "Number of Accidents"):
    counts = df.groupby(column_name)[column_name].count()

    if label_dict:
        x=[label_dict[index] for index in counts.index.values]
        x_range = x
    else:
        x = [index for index in counts.index.values]

        if counts.index.dtype == str:
            x_range = x
        else:
            x_range = (min(x), max(x))

    bar_source = ColumnDataSource(dict(x=x, y=counts.values))

    p_bar = figure(x_range=x_range, aspect_ratio=4, title=title,
                   toolbar_location=None, tools="", x_axis_label=x_label, y_axis_label=y_label, y_range= ranges.Range1d(start=0,end=1.3 * max(bar_source.data["y"])), height_policy="max", width_policy="max")

    p_bar.vbar(x="x", top="y", width=1.1, source=bar_source)

    p_bar.xgrid.grid_line_color = None

    labels = LabelSet(x='x', y='y', text='y', level='glyph',
                      text_align='center', y_offset=5, source=bar_source)

    p_bar.add_layout(labels)
    return p_bar


def _generate_pie_chart(df, column_name, label_dict=None, title="LABEL"):
    counts = df.groupby(column_name)[column_name].count()
    pie_data = pd.DataFrame(columns=["labels", "count", "angle"])
    pie_data["labels"] = [label_dict[idx] for idx in counts.index.values]
    pie_data["count"] = counts.values

    #Deal with issues of having more than 20 categories by erasing the least important ones TODO some them in their own
    #column
    pie_data = pie_data.sort_values(by=['count']).head(20).sort_values(by=['labels'])
    pie_data['angle'] = pie_data['count']/pie_data['count'].sum() * 2*pi

    if len(pie_data) < 3:
        pie_data['color'] = Category20c[3][:len(pie_data)]
    else:
        pie_data['color'] = Category20c[len(pie_data)]

    pie_data['legend'] = pie_data["labels"] + ": " + pie_data["count"].astype(str)

    pie = figure(height=350, title=title, toolbar_location=None,
                 tools="hover", tooltips="@labels: @count", x_range=(-0.5, 1.5))

    pie.wedge(x=0, y=1, radius=0.4,
              start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
              line_color="white", fill_color='color', legend_field='legend', source=pie_data)

    pie.axis.axis_label = None
    pie.legend.title = "Total: " + str(pie_data["count"].sum())
    pie.legend.label_text_font_size = '5pt'
    pie.axis.visible = False
    pie.grid.grid_line_color = None
    return pie
