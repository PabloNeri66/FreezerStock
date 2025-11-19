from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import metrics
import json


@login_required(login_url='login')
def home(request):
    geladinho_metrics = metrics.get_geladinho_metrics()
    sales_metrics = metrics.get_sales_metrics()
    daily_sales_data = metrics.get_daily_sales_data()
    daily_sales_quantity_data = metrics.get_daily_sales_quantity_data()
    graphic_geladinho_flavor_metric, geladinho_colors = metrics.get_graphic_geladinho_flavor_metric()

    context = {
        'geladinho_metrics': geladinho_metrics,
        'sales_metrics': sales_metrics,
        'daily_sales_data': json.dumps(daily_sales_data),
        'daily_sales_quantity_data': json.dumps(daily_sales_quantity_data),
        'geladinho_count_by_flavor': json.dumps(graphic_geladinho_flavor_metric),
        'geladinho_colors': geladinho_colors,
    }

    return render(request, 'home.html', context)
