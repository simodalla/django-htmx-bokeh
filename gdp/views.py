import math

from django.db.models import Max, Min
from django.shortcuts import render

from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.plotting import figure

from .models import GDP


def index(request):
    # define which year we want the data from
    max_year = GDP.objects.aggregate(max_yr=Max("year"))["max_yr"]
    min_year = GDP.objects.aggregate(min_yr=Min("year"))["min_yr"]
    year = request.GET.get("year", max_year)

    # define number of countires to fetch
    count = int(request.GET.get("count", 10))

    gdps = GDP.objects.filter(year=year).order_by("gdp").reverse()[:count]

    country_names = [d.country for d in gdps]
    country_gdps = [d.gdp for d in gdps]

    cds = ColumnDataSource(
        data=dict(
            country_names=country_names,
            country_gdps=country_gdps,
        )
    )

    fig = figure(x_range=country_names, height=500, title=f"Top {count} GDPs ({year})")
    fig.title.align = "center"
    fig.title.text_font_size = "1.5em"
    fig.yaxis[0].formatter = NumeralTickFormatter(format="$0.0a")
    fig.xaxis.major_label_orientation = math.pi / 4

    fig.vbar(source=cds, x="country_names", top="country_gdps", width=0.8)
    tooltips = [("Country", "@country_names"), ("GDP", "@country_gdps{,}")]
    fig.add_tools(HoverTool(tooltips=tooltips))

    script, div = components(fig)
    context = {
        "script": script,
        "div": div,
        "years": range(min_year, max_year + 1),
        "count": count,
        "year_selected": year,
    }

    template = "partials/gdp-bar.html" if request.htmx else "index.html"
    return render(request, template, context)
